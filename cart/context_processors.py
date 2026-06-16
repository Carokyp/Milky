from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product
from accounts.models import UserCustomer


def cart_contents(request):
    """Make cart contents available across all templates"""
    cart_items = []
    total = Decimal("0.00")
    product_count = 0
    cart = request.session.get("cart", {})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({
            "product_id": product_id,
            "quantity": quantity,
            "product": product,
            "subtotal": quantity * product.price,
        })

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
    if request.user.is_authenticated:
        user_customer = UserCustomer.objects.filter(user=request.user).first()
        if user_customer and user_customer.customer.promo_discount:
            promo_discount = user_customer.customer.promo_discount
            discount_rate = Decimal(str(settings.PROMO_DISCOUNT_PERCENTAGE)) / 100
            grand_total = (grand_total * (1 - discount_rate)).quantize(
                Decimal("0.01")
            )

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
        "remaining_for_free_delivery": remaining,
        "free_delivery_threshold": free_delivery_threshold,
        "delivery": delivery,
        "grand_total": grand_total,
        "promo_discount": promo_discount,
    }

    return context
