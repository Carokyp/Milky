from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """Make cart contents available across all templates"""
    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get("cart", {})

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
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

    if total < settings.FREE_DELIVERY_THRESHOLD:
        remaining = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        remaining = 0

    context = {
        "cart_items": cart_items,
        "total": total,
        "product_count": product_count,
        "remaining_for_free_delivery": remaining,
    }

    return context
