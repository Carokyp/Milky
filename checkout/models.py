from django.db import models
from accounts.models import Customer
from products.models import Product
from django_countries.fields import CountryField
import uuid
from decimal import Decimal


def generate_reference_code():
    return f"ORDER-{uuid.uuid4().hex[:8].upper()}"


class Order(models.Model):

    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Completed'),
        (2, 'Cancelled'),
    ]

    # Identifiers
    reference_code = models.CharField(max_length=100, unique=True, default=generate_reference_code, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)  # 0: pending, 1: completed, 2: cancelled
    created_at = models.DateTimeField(auto_now_add=True)

    # Financials
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=Decimal('0.00'))

    # Invoice details
    invoice_name = models.CharField(max_length=100)
    invoice_surname = models.CharField(max_length=100)
    invoice_phone = models.CharField(max_length=20)
    invoice_address = models.CharField(max_length=255)
    invoice_city = models.CharField(max_length=100)
    invoice_county = models.CharField(max_length=100, null=True, blank=True)
    invoice_postcode = models.CharField(max_length=20, null=True, blank=True)
    invoice_country = CountryField(max_length=100)

    # Delivery details
    delivery_name = models.CharField(max_length=100)
    delivery_surname = models.CharField(max_length=100)
    delivery_phone = models.CharField(max_length=20)
    delivery_address = models.CharField(max_length=255)
    delivery_city = models.CharField(max_length=100)
    delivery_county = models.CharField(max_length=100, null=True, blank=True)
    delivery_postcode = models.CharField(max_length=20, null=True, blank=True)
    delivery_country = CountryField(max_length=100)

    @property
    def grand_total(self):
        order_total = self.order_total or Decimal('0.00')
        delivery_cost = self.delivery_cost or Decimal('0.00')
        return order_total + delivery_cost

    def __str__(self):
        return f"Order {self.reference_code} - {self.customer.name} {self.customer.surname}"


class OrderItem(models.Model):
    # Relationships
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Product snapshot
    sku = models.CharField(max_length=255, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Order info
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order {self.order.reference_code} | {self.product.name} (SKU: {self.sku}) x {self.quantity}"


class Payment(models.Model):

    STATUS_CHOICES = [
        (0, 'Pending'),
        (1, 'Completed'),
        (2, 'Failed'),
    ]

    # Relationship
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')

    # Payment info
    stripe_pid = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status_display = dict(self.STATUS_CHOICES).get(self.status, 'Unknown')
        return f"Payment for Order {self.order.reference_code} - Status: {status_display}"
