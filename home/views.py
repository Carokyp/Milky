from django.shortcuts import render

from products.models import Product


def index(request):
    """Render the home page with the available featured products."""
    products = Product.objects.filter(featured=True, is_available=True)
    return render(request, "home/index.html", {"products": products})
