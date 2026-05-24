from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from products.models import Product

# Create your views here.


def cart_view(request):
    """View for the shopping cart page."""
    return render(request, "cart.html")


def add_to_cart(request, product_id):
    """Add a product to the cart"""
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity

    request.session["cart"] = cart
    messages.success(request, f"{product.name} has been added to your cart!")
    return redirect(request.POST.get("redirect_url", "/"))


def remove_from_cart(request, product_id):
    """Remove a product from the cart"""
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        messages.success(request, f"{product.name} has been removed from your cart!")

    request.session["cart"] = cart
    return redirect("view_cart")


def update_cart(request, product_id):
    """Update the quantity of a product in the cart"""
    product = get_object_or_404(Product, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))
    cart = request.session.get("cart", {})

    if quantity >= 1:
        cart[str(product_id)] = quantity
        messages.success(request, f"{product.name} has been updated in your cart!")
    else:
        del cart[str(product_id)]
        messages.success(request, f"{product.name} has been removed from your cart!")

    request.session["cart"] = cart
    return redirect("view_cart")
