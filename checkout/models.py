import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django_countries.fields import CountryField

from accounts.models import Customer
from products.models import Product


def generate_reference_code():
    """Return a random order reference like 'ORDER-1A2B3C4D'."""
    return f"ORDER-{uuid.uuid4().hex[:8].upper()}"


class Order(models.Model):
    """A customer order, its delivery/invoice details and totals."""

    # Order lifecycle states used in the admin and checkout flow.
    STATUS_CHOICES = [
        (0, "Pending"),
        (1, "Completed"),
        (2, "Cancelled"),
    ]

    # Core order identity and ownership.
    reference_code = models.CharField(
        max_length=100,
        unique=True,
        default=generate_reference_code,
        editable=False,
    )
    stripe_pid = models.CharField(max_length=254, null=True, blank=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    status = models.IntegerField(
        default=0, choices=STATUS_CHOICES
    )  # 0: pending, 1: completed, 2: cancelled
    created_at = models.DateTimeField(auto_now_add=True)

    # Order totals, stored so they can be reused in templates and admin.
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=Decimal("0.00")
    )
    promo_discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    # Invoice address fields.
    invoice_name = models.CharField(max_length=100, blank=True)
    invoice_surname = models.CharField(max_length=100, blank=True)
    invoice_phone = models.CharField(max_length=20, blank=True)
    invoice_address = models.CharField(max_length=255, blank=True)
    invoice_city = models.CharField(max_length=100, blank=True)
    invoice_county = models.CharField(max_length=100, null=True, blank=True)
    invoice_postcode = models.CharField(max_length=20, null=True, blank=True)
    invoice_country = CountryField(max_length=100, blank=True)

    # Delivery address fields.
    delivery_name = models.CharField(max_length=100)
    delivery_surname = models.CharField(max_length=100)
    delivery_phone = models.CharField(max_length=20)
    delivery_address = models.CharField(max_length=255)
    delivery_city = models.CharField(max_length=100)
    delivery_county = models.CharField(max_length=100, null=True, blank=True)
    delivery_postcode = models.CharField(
        max_length=20, null=True, blank=True
    )
    delivery_country = CountryField(max_length=100)

    email = models.EmailField(max_length=254)

    @property
    def grand_total(self):
        """Return order_total plus delivery, minus any promo discount."""
        order_total = self.order_total or Decimal("0.00")
        delivery_cost = self.delivery_cost or Decimal("0.00")
        grand_total = order_total + delivery_cost

        if self.promo_discount_percent:
            discount_rate = self.promo_discount_percent / Decimal("100")
            grand_total = grand_total * (Decimal("1") - discount_rate)

        return grand_total.quantize(Decimal("0.01"))

    def recalculate_delivery_cost(self):
        """Recompute delivery_cost from the current order subtotal."""
        order_total = self.order_total or Decimal("0.00")

        # A zero subtotal (no items, or zero-valued items) means free
        # shipping rather than the normal delivery fee.
        if order_total == Decimal("0.00"):
            self.delivery_cost = Decimal("0.00")
            return

        free_delivery_threshold = Decimal(
            str(settings.FREE_DELIVERY_THRESHOLD)
        )
        delivery_cost = Decimal(str(settings.DELIVERY_COST))

        if order_total < free_delivery_threshold:
            self.delivery_cost = delivery_cost
        else:
            self.delivery_cost = Decimal("0.00")

    def save(self, *args, **kwargs):
        """Recalculate delivery cost before saving."""
        self.recalculate_delivery_cost()
        super().save(*args, **kwargs)

    def __str__(self):
        """Return a human-readable label for the admin."""
        if self.customer:
            return (
                f"Order {self.reference_code} - "
                f"{self.customer.name} {self.customer.surname}"
            )
        return (
            f"Order {self.reference_code} - "
            f"{self.delivery_name} {self.delivery_surname} - {self.email}"
        )


class OrderItem(models.Model):
    """A single product line within an order."""

    # Link each line item to its order and purchased product.
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Snapshot of the product at the time of purchase.
    sku = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Quantity and line total for this item.
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Gift a Can set when this line is the one can bought for a friend.
    is_gift = models.BooleanField(default=False)
    gift_contact = models.ForeignKey(
        "accounts.Contact", on_delete=models.SET_NULL, null=True, blank=True
    )
    gift_message = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        """Sync total_price and the parent order's total on every save."""
        # Fall back to the product's price if none was set explicitly.
        if self.unit_price is None and getattr(self, "product_id", None):
            self.unit_price = self.product.price

        # Keep the line total in sync with quantity and unit price.
        if self.unit_price is not None:
            self.total_price = self.unit_price * self.quantity

        # Save the line item first, then refresh the parent order total.
        super().save(*args, **kwargs)
        self.order.order_total = OrderItem.objects.filter(
            order=self.order
        ).aggregate(total=Sum("total_price"))["total"] or Decimal("0.00")
        self.order.save()

    def __str__(self):
        """Return a human-readable label for the admin."""
        return (
            f"Order {self.order.reference_code} | "
            f"{self.product.name} (SKU: {self.sku}) x {self.quantity}"
        )
