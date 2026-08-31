# Adapted from the Code Institute "Boutique Ado" walkthrough (bag context
# processor), extended here with the Gift a Can session item and its discount.
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings

from products.models import Product
from accounts.models import Contact


def gift_item_from_session(request):
    """Look up the gift can's product/contact from the current session.

    Returns None if there is no gift in progress, or if its product has
    since been deleted (in which case the stale gift is cleared).
    """
    gift = request.session.get("gift")
    if not gift:
        return None

    product = Product.objects.filter(pk=gift["product_id"]).first()
    if product is None:
        request.session.pop("gift", None)
        return None
    contact = Contact.objects.filter(pk=gift["contact_id"]).first()

    return {
        "product": product,
        "contact": contact,
        "personal_message": gift.get("personal_message", ""),
        "price": product.price,
    }


def cart_contents(request):
    """Make cart contents available across all templates."""
    cart_items = []
    total = Decimal("0.00")
    product_count = 0
    cart = request.session.get("cart", {})

    # Skip and prune any product that has since been deleted, so a stale
    # cart entry never breaks page rendering.
    missing = []
    for product_id, quantity in cart.items():
        product = Product.objects.filter(pk=product_id).first()
        if product is None:
            missing.append(product_id)
            continue
        total += quantity * product.price
        product_count += quantity
        cart_items.append(
            {
                "product_id": product_id,
                "quantity": quantity,
                "product": product,
                "subtotal": quantity * product.price,
            }
        )

    if missing:
        for product_id in missing:
            cart.pop(product_id, None)
        request.session["cart"] = cart

    gift_item = gift_item_from_session(request)
    if gift_item:
        total += gift_item["price"]
        product_count += 1

    free_delivery_threshold = Decimal(str(settings.FREE_DELIVERY_THRESHOLD))
    delivery_cost = Decimal(str(settings.DELIVERY_COST))

    if total < free_delivery_threshold:
        remaining = (free_delivery_threshold - total).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        delivery = delivery_cost
    else:
        remaining = Decimal("0.00")
        delivery = Decimal("0.00")

    total = total.quantize(Decimal("0.01"))
    delivery = delivery.quantize(Decimal("0.01"))
    grand_total = (total + delivery).quantize(Decimal("0.01"))

    promo_discount = None
    if gift_item:
        promo_discount = Decimal(str(settings.PROMO_DISCOUNT_PERCENTAGE))
        discount_rate = promo_discount / 100
        grand_total = (grand_total * (1 - discount_rate)).quantize(
            Decimal("0.01")
        )

    return {
        "cart_items": cart_items,
        "gift_item": gift_item,
        "total": total,
        "product_count": product_count,
        "remaining_for_free_delivery": remaining,
        "delivery": delivery,
        "grand_total": grand_total,
        "promo_discount": promo_discount,
    }
