import stripe
import json
from decimal import Decimal

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST

from accounts.models import Customer
from accounts.models import UserCustomer
from cart.context_processors import cart_contents

from .email_utils import build_confirmation_email_context
from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product

stripe.api_key = settings.STRIPE_SECRET_KEY


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        order_data = request.session.get("order_data", {})
        # Remove invoice fields to reduce metadata size
        essential_data = {
            "delivery_name": order_data.get("delivery_name", ""),
            "delivery_surname": order_data.get("delivery_surname", ""),
            "delivery_phone": order_data.get("delivery_phone", ""),
            "delivery_address": order_data.get("delivery_address", ""),
            "delivery_city": order_data.get("delivery_city", ""),
            "delivery_county": order_data.get("delivery_county", ""),
            "delivery_postcode": order_data.get("delivery_postcode", ""),
            "delivery_country": order_data.get("delivery_country", ""),
            "email": order_data.get("email", ""),
            "same_as_delivery": order_data.get("same_as_delivery", True),
            "save_info": order_data.get("save_info", False),
        }
        metadata = {
            "user_id": str(request.user.id) if request.user.is_authenticated else "",
            "save_info": str(request.POST.get("save-info") or ""),
            "cart": json.dumps(request.session.get("cart", {})),
            "order_data": json.dumps(essential_data),
            "gift": json.dumps(request.session.get("gift", {})),
        }
        stripe.PaymentIntent.modify(pid, metadata=metadata)
        return HttpResponse(status=200)
    except Exception as e:
        print(f"Cache checkout error: {e}")  # Log the error for debugging
        messages.error(request, "Sorry, your payment cannot be processed right now.")
        return HttpResponse(content=e, status=400)


def checkout(request):

    cart = request.session.get("cart", {})
    if not cart and not request.session.get("gift"):
        messages.error(request, "Your cart is empty.")
        return redirect(reverse("products"))

    if request.user.is_authenticated:
        user_customers = UserCustomer.objects.filter(user=request.user).first()
        customer = user_customers.customer if user_customers else None

        if not customer:
            customer = Customer.objects.create()
            UserCustomer.objects.create(
                user=request.user,
                customer=customer,
                enabled=True,
            )

        order_form = OrderForm(
            initial={
                "delivery_name": customer.name or "",
                "delivery_surname": customer.surname or "",
                "delivery_phone": customer.phone_number or "",
                "delivery_address": customer.address or "",
                "delivery_city": customer.city or "",
                "delivery_county": customer.county or "",
                "delivery_postcode": customer.postal_code or "",
                "delivery_country": customer.country or "",
            },
            user_authenticated=True,
        )
    else:
        customer = None
        order_form = OrderForm(user_authenticated=False)

    if request.method == "POST":
        form = OrderForm(request.POST, user_authenticated=request.user.is_authenticated)
        if form.is_valid():
            same_as_delivery = request.POST.get("same-as-delivery")
            request.session["order_data"] = {
                "delivery_name": form.cleaned_data["delivery_name"],
                "delivery_surname": form.cleaned_data["delivery_surname"],
                "delivery_phone": form.cleaned_data["delivery_phone"],
                "delivery_address": form.cleaned_data["delivery_address"],
                "delivery_city": form.cleaned_data["delivery_city"],
                "delivery_county": form.cleaned_data.get("delivery_county", ""),
                "delivery_postcode": form.cleaned_data.get("delivery_postcode", ""),
                "delivery_country": str(form.cleaned_data["delivery_country"]),
                "email": (
                    request.user.email
                    if request.user.is_authenticated
                    else form.cleaned_data.get("email", "")
                ),
                "same_as_delivery": bool(same_as_delivery),
                "invoice_name": form.cleaned_data.get("invoice_name", ""),
                "invoice_surname": form.cleaned_data.get("invoice_surname", ""),
                "invoice_phone": form.cleaned_data.get("invoice_phone", ""),
                "invoice_address": form.cleaned_data.get("invoice_address", ""),
                "invoice_city": form.cleaned_data.get("invoice_city", ""),
                "invoice_county": form.cleaned_data.get("invoice_county", ""),
                "invoice_postcode": form.cleaned_data.get("invoice_postcode", ""),
                "invoice_country": str(form.cleaned_data.get("invoice_country", "")),
                "save_info": bool(request.POST.get("save-info")),
            }
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"status": "error"}, status=400)

    cart_data = cart_contents(request)

    payment_intent = stripe.PaymentIntent.create(
        amount=int(cart_data["grand_total"] * 100),
        currency="usd",
        metadata={
            "user_id": str(request.user.id) if request.user.is_authenticated else ""
        },
    )

    return render(
        request,
        "checkout/checkout.html",
        {
            "form": order_form,
            "client_secret": payment_intent.client_secret,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        },
    )


def checkout_success(request):
    pid = request.GET.get("payment_intent")
    order_data = request.session.get("order_data", {})
    cart = request.session.get("cart", {})
    gift = request.session.get("gift")

    if not order_data or (not cart and not gift):
        messages.error(request, "Something went wrong. Please try again.")
        return redirect(reverse("checkout"))

    if request.user.is_authenticated:
        user_customers = UserCustomer.objects.filter(user=request.user).first()
        customer = user_customers.customer if user_customers else None
    else:
        customer = None

    same_as_delivery = order_data.get("same_as_delivery", True)

    order = Order(
        customer=customer,
        stripe_pid=pid,
        delivery_name=order_data["delivery_name"],
        delivery_surname=order_data["delivery_surname"],
        delivery_phone=order_data["delivery_phone"],
        delivery_address=order_data["delivery_address"],
        delivery_city=order_data["delivery_city"],
        delivery_county=order_data.get("delivery_county", ""),
        delivery_postcode=order_data.get("delivery_postcode", ""),
        delivery_country=order_data["delivery_country"],
        email=order_data.get("email", ""),
        invoice_name=(
            order_data["delivery_name"]
            if same_as_delivery
            else order_data.get("invoice_name", "")
        ),
        invoice_surname=(
            order_data["delivery_surname"]
            if same_as_delivery
            else order_data.get("invoice_surname", "")
        ),
        invoice_phone=(
            order_data["delivery_phone"]
            if same_as_delivery
            else order_data.get("invoice_phone", "")
        ),
        invoice_address=(
            order_data["delivery_address"]
            if same_as_delivery
            else order_data.get("invoice_address", "")
        ),
        invoice_city=(
            order_data["delivery_city"]
            if same_as_delivery
            else order_data.get("invoice_city", "")
        ),
        invoice_county=(
            order_data.get("delivery_county", "")
            if same_as_delivery
            else order_data.get("invoice_county", "")
        ),
        invoice_postcode=(
            order_data.get("delivery_postcode", "")
            if same_as_delivery
            else order_data.get("invoice_postcode", "")
        ),
        invoice_country=(
            order_data["delivery_country"]
            if same_as_delivery
            else order_data.get("invoice_country", "")
        ),
        promo_discount_percent=(
            Decimal(str(settings.PROMO_DISCOUNT_PERCENTAGE)) if gift else None
        ),
    )

    cart_data = cart_contents(request)
    order.order_total = cart_data["total"]
    order.save()

    # Create order items
    for item_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                sku=product.sku,
                unit_price=product.price,
                quantity=quantity,
                total_price=product.price * quantity,
            )
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            order.delete()
            return redirect(reverse("cart"))

    if gift:
        gift_product = get_object_or_404(Product, pk=gift["product_id"])
        OrderItem.objects.create(
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

    # Save delivery info to profile if checkbox was ticked
    save_info = order_data.get("save_info")
    if save_info and customer:
        customer.name = order_data["delivery_name"]
        customer.surname = order_data["delivery_surname"]
        customer.phone_number = order_data["delivery_phone"]
        customer.address = order_data["delivery_address"]
        customer.city = order_data["delivery_city"]
        customer.county = order_data.get("delivery_county", "")
        customer.postal_code = order_data.get("delivery_postcode", "")
        customer.country = order_data["delivery_country"]
        customer.save()

    # Save last order reference for non-authenticated users
    request.session["last_order"] = order.reference_code

    # Clear session
    if "cart" in request.session:
        del request.session["cart"]
    del request.session["order_data"]
    request.session.pop("gift", None)

    messages.success(
        request,
        f"Order {order.reference_code} placed successfully! You will receive a confirmation email at {order.email} shortly.",
        extra_tags="order",
    )
    return redirect(reverse("order_confirmation", args=[order.reference_code]))


def order_confirmation(request, reference_code):
    if request.user.is_authenticated:
        order = get_object_or_404(
            Order,
            reference_code=reference_code,
            customer__usercustomer__user=request.user,
        )
    else:
        last_order = request.session.get("last_order")
        if last_order != reference_code:
            return redirect(reverse("home"))
        order = get_object_or_404(Order, reference_code=reference_code)

    return render(request, "checkout/checkout_success.html", {"order": order})


@login_required
def preview_confirmation_email(request):
    """Render the real confirmation email in the browser, for styling work.
    Store-owner only — shows real customer data from the most recent order."""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    order = Order.objects.order_by("-created_at").first()
    if not order:
        return HttpResponse("No order in the database yet — place a test order first.")

    context = build_confirmation_email_context(request, order, settings.DEFAULT_FROM_EMAIL)
    html_body = render_to_string("checkout/confirmation_email_body.html", context)
    return HttpResponse(html_body)
