from django.contrib import messages
from django.shortcuts import redirect, render

from products.models import Product


def index(request):
    """Render the home page with the available featured products."""
    products = Product.objects.filter(featured=True, is_available=True)
    return render(request, "home/index.html", {"products": products})


# TODO: Remove test views before deployment


def test_404(request):
    from milky.views import handler404

    return handler404(request, Exception())


def test_403(request):
    from milky.views import handler403

    return handler403(request, Exception())


def test_405(request):
    from milky.views import handler405

    return handler405(request, Exception())


def test_500(request):
    from milky.views import handler500

    return handler500(request)


def test_success(request):
    messages.success(request, "Product added to your cart!")
    return redirect("home")


def test_warning(request):
    messages.warning(request, "This is a warning!")
    return redirect("home")


def test_error(request):
    messages.error(request, "Something went wrong!")
    return redirect("home")


def test_info(request):
    messages.info(request, "This is an info message!")
    return redirect("home")


def test_change_password(request):
    from django.contrib.auth import get_user_model
    from allauth.account.forms import ResetPasswordKeyForm

    user = (
        request.user
        if request.user.is_authenticated
        else get_user_model().objects.first()
    )
    form = ResetPasswordKeyForm(user=user, temp_key="preview")
    return render(
        request,
        "account/password_reset_from_key.html",
        {"form": form, "action_url": "#"},
    )
