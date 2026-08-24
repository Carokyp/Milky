from decimal import Decimal

from django.conf import settings

from products.models import Product

from .models import OrderItem


def build_order_kwargs(order_data, customer, gift):
    """Build the shared Order() field values from session order_data.

    Delivery fields come straight from order_data. Invoice fields fall
    back to the matching delivery field when "same_as_delivery" is set
    (the default). Used by both the checkout view and the Stripe
    webhook handler, which each add their own status/stripe_pid.
    """
    same_as_delivery = order_data.get("same_as_delivery", True)

    def invoice(field_suffix):
        delivery_value = order_data.get(f"delivery_{field_suffix}", "")
        if same_as_delivery:
            return delivery_value
        return order_data.get(f"invoice_{field_suffix}", "")

    return {
        "customer": customer,
        "delivery_name": order_data.get("delivery_name", ""),
        "delivery_surname": order_data.get("delivery_surname", ""),
        "delivery_phone": order_data.get("delivery_phone", ""),
        "delivery_address": order_data.get("delivery_address", ""),
        "delivery_city": order_data.get("delivery_city", ""),
        "delivery_county": order_data.get("delivery_county", ""),
        "delivery_postcode": order_data.get("delivery_postcode", ""),
        "delivery_country": order_data.get("delivery_country", ""),
        "email": order_data.get("email", ""),
        "invoice_name": invoice("name"),
        "invoice_surname": invoice("surname"),
        "invoice_phone": invoice("phone"),
        "invoice_address": invoice("address"),
        "invoice_city": invoice("city"),
        "invoice_county": invoice("county"),
        "invoice_postcode": invoice("postcode"),
        "invoice_country": invoice("country"),
        "promo_discount_percent": (
            Decimal(str(settings.PROMO_DISCOUNT_PERCENTAGE))
            if gift else None
        ),
    }


def create_order_item(order, product_id, quantity):
    """Create an OrderItem for one cart line."""
    product = Product.objects.get(id=product_id)
    return OrderItem.objects.create(
        order=order,
        product=product,
        sku=product.sku,
        unit_price=product.price,
        quantity=quantity,
        total_price=product.price * quantity,
    )


def create_gift_order_item(order, gift, gift_product):
    """Create the OrderItem for a gifted can."""
    return OrderItem.objects.create(
        order=order,
        product=gift_product,
        sku=gift_product.sku,
        unit_price=gift_product.price,
        quantity=1,
        total_price=gift_product.price,
        is_gift=True,
        gift_contact_id=gift["contact_id"],
        gift_message=gift.get("personal_message", ""),
    )
