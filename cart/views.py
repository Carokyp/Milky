from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
from django.conf import settings
from django.utils.html import format_html
from products.models import Product
from .context_processors import gift_item_from_session


def _parse_quantity(raw_quantity, default=1):
    try:
        return int(raw_quantity)
    except (TypeError, ValueError):
        return default


def cart_view(request):
    """View for the shopping cart page."""
    return render(request, "cart/cart.html")


def _cart_totals_json(request, cart, product_id=None, quantity=None):
    """Helper function to calculate cart totals, subtotal and delivery costs."""
    total = Decimal("0.00")
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=pid)
        total += Decimal(qty) * product.price

    product_count = sum(int(q) for q in cart.values())

    gift_item = gift_item_from_session(request)
    if gift_item:
        total += gift_item["price"]
        product_count += 1

    free_delivery_threshold = Decimal(str(settings.FREE_DELIVERY_THRESHOLD))
    delivery_cost = Decimal(str(settings.DELIVERY_COST))

    if total < free_delivery_threshold:
        remaining = (free_delivery_threshold - total).quantize(Decimal("0.01"))
        delivery = delivery_cost
    else:
        remaining = Decimal("0.00")
        delivery = Decimal("0.00")

    grand_total = (total + delivery).quantize(Decimal("0.01"))

    if gift_item:
        discount_rate = Decimal(str(settings.PROMO_DISCOUNT_PERCENTAGE)) / 100
        grand_total = (grand_total * (1 - discount_rate)).quantize(Decimal("0.01"))

    total = total.quantize(Decimal("0.01"))

    data = {
        "total": str(total),
        "delivery": str(delivery),
        "grand_total": str(grand_total),
        "remaining_for_free_delivery": str(remaining),
        "product_count": product_count,
    }

    if product_id is not None:
        prod = get_object_or_404(Product, pk=product_id)
        item_qty = (
            int(quantity) if quantity is not None else int(cart.get(str(product_id), 0))
        )
        item_subtotal = (Decimal(item_qty) * prod.price).quantize(Decimal("0.01"))
        data.update(
            {
                "product_id": product_id,
                "item_subtotal": str(item_subtotal),
            }
        )

    return data


def add_to_cart(request, product_id):
    """Add a product to the cart"""
    try:
        product = get_object_or_404(Product, pk=product_id)

        # Vérification disponibilité en premier !
        if not product.is_available:
            messages.error(request, 'This product is not available.')
            return redirect(reverse('product_detail', args=[product_id]))

        quantity = _parse_quantity(request.POST.get("quantity"))
        quantity = max(1, quantity)
        cart = request.session.get("cart", {})
        key = str(product_id)
        existing = int(cart.get(key, 0))

        new_total = min(existing + quantity, 99)
        cart[key] = new_total
        request.session["cart"] = cart

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                _cart_totals_json(request, cart, product_id=product_id), status=200
            )

        if existing >= 99:
            messages.info(request, f"{product.name} is already at the maximum quantity (99).")
        elif new_total < existing + quantity:
            messages.warning(request, f"Requested quantity was reduced so {product.name} is capped at 99 in your cart.")
        else:
            messages.success(
                request,
                format_html("<strong>{}</strong> has been added to your cart!", product.name),
                extra_tags="cart",
            )

        return redirect(request.POST.get("redirect_url", "/"))

    except Exception as e:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": str(e)}, status=500)
        messages.error(request, f"Error adding to cart: {e}")
        return redirect(request.POST.get("redirect_url", "/"))


def update_cart(request, product_id):
    """Update the quantity of a product in the cart"""
    try:
        product = get_object_or_404(Product, pk=product_id)
        quantity = _parse_quantity(request.POST.get("quantity"))
        cart = request.session.get("cart", {})

        if quantity >= 1:
            cart[str(product_id)] = quantity
        else:
            if str(product_id) in cart:
                del cart[str(product_id)]

        request.session["cart"] = cart

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                _cart_totals_json(request, cart, product_id=product_id, quantity=quantity),
                status=200,
            )

        messages.success(
            request,
            format_html("<strong>{}</strong> has been updated in your cart!", product.name),
            extra_tags="cart-update",
        )
        return redirect("view_cart")

    except Exception as e:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": str(e)}, status=500)
        messages.error(request, f"Error updating cart: {e}")
        return redirect("view_cart")


def remove_from_cart(request, product_id):
    """Remove a product from the cart"""
    try:
        product = get_object_or_404(Product, pk=product_id)
        cart = request.session.get("cart", {})

        if str(product_id) in cart:
            del cart[str(product_id)]

        request.session["cart"] = cart

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(_cart_totals_json(request, cart), status=200)

        messages.success(
            request,
            format_html("<strong>{}</strong> has been removed from your cart!", product.name),
            extra_tags="cart-remove",
        )
        return redirect("view_cart")

    except Exception as e:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": str(e)}, status=500)
        messages.error(request, f"Error removing from cart: {e}")
        return redirect("view_cart")


def remove_gift(request):
    """Remove the gift can from the current order, freeing up Gift a Can again."""
    try:
        request.session.pop("gift", None)
        cart = request.session.get("cart", {})

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(_cart_totals_json(request, cart), status=200)

        return redirect("view_cart")

    except Exception as e:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": str(e)}, status=500)
        messages.error(request, f"Error removing gift: {e}")
        return redirect("view_cart")
