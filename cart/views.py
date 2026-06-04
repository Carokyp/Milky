from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
from django.conf import settings
from products.models import Product


def _parse_quantity(raw_quantity, default=1):
    try:
        return int(raw_quantity)
    except (TypeError, ValueError):
        return default


def cart_view(request):
    """View for the shopping cart page."""
    return render(request, "cart/cart.html")


def _cart_totals_json(cart, product_id=None, quantity=None):
    """Helper function to calculate cart totals, subtotal and delivery costs."""
    total = Decimal("0.00")
    for pid, qty in cart.items():
        product = get_object_or_404(Product, pk=pid)
        total += Decimal(qty) * product.price

    free_delivery_threshold = Decimal(str(settings.FREE_DELIVERY_THRESHOLD))
    delivery_cost = Decimal(str(settings.DELIVERY_COST))

    if total < free_delivery_threshold:
        remaining = (free_delivery_threshold - total).quantize(Decimal("0.01"))
        delivery = delivery_cost
    else:
        remaining = Decimal("0.00")
        delivery = Decimal("0.00")

    grand_total = (total + delivery).quantize(Decimal("0.01"))
    total = total.quantize(Decimal("0.01"))
    product_count = sum(int(q) for q in cart.values())

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
                _cart_totals_json(cart, product_id=product_id), status=200
            )

        if existing >= 99:
            messages.info(
                request, f"{product.name} is already at the maximum quantity (99)."
            )
        elif new_total < existing + quantity:
            messages.warning(
                request,
                f"Requested quantity was reduced so {product.name} is capped at 99 in your cart.",
            )
        else:
            messages.success(
                request,
                f"{product.name} has been added to your cart!",
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
                _cart_totals_json(cart, product_id=product_id, quantity=quantity),
                status=200,
            )

        messages.success(request, f"{product.name} has been updated in your cart!")
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
            return JsonResponse(_cart_totals_json(cart), status=200)

        messages.success(request, f"{product.name} has been removed from your cart!")
        return redirect("view_cart")

    except Exception as e:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": str(e)}, status=500)
        messages.error(request, f"Error removing from cart: {e}")
        return redirect("view_cart")
