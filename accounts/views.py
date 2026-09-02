from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string

from checkout.models import Order
from milky.email_utils import build_email_font_urls

from .forms import CustomerForm, GiftACanForm
from .models import Contact, UserCustomer


@login_required
def profile_view(request):
    """Display and update the logged-in user's customer profile."""
    user_customers = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customers.customer if user_customers else None
    orders = Order.objects.filter(customer=customer) if customer else None
    if customer:
        contacts = list(customer.contact_set.all())  # type: ignore
    else:
        contacts = []
    for contact in contacts:
        contact.edit_form = GiftACanForm(instance=contact)
    contact_form = GiftACanForm()
    active_tab = request.session.pop("profile_active_tab", "profile")

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            if not user_customers:
                UserCustomer.objects.create(
                    user=request.user, customer=form.instance
                )
            messages.success(
                request,
                "Your profile has been updated successfully.",
                extra_tags="profile",
            )
            return redirect("profile")
    else:
        form = CustomerForm(instance=customer)

    context = {
        "customer": customer,
        "form": form,
        "orders": orders,
        "contacts": contacts,
        "contact_form": contact_form,
        "active_tab": active_tab,
    }
    return render(request, "accounts/profile.html", context)


def orders_history_view(request, reference_code):
    """View for the user's order history."""
    order = get_object_or_404(
        Order,
        reference_code=reference_code,
        customer__usercustomer__user=request.user,
    )
    return render(
        request,
        "checkout/checkout_success.html",
        {
            "order": order,
            "from_profile": True,
        },
    )


@login_required
def add_contact_view(request):
    """Add a new contact for the logged-in user's customer profile."""
    user_customer = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customer.customer if user_customer else None

    if not customer:
        messages.error(request, "Please complete your profile first.")
        return redirect("profile")

    if request.method == "POST":
        form = GiftACanForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.customer = customer
            contact.ip_address = request.META.get("REMOTE_ADDR", "")
            contact.save()
            messages.success(
                request, "Contact added successfully.", extra_tags="contact"
            )
        else:
            messages.error(request, "Failed to add contact.")

    request.session["profile_active_tab"] = "contacts"
    return redirect("profile")


@login_required
def edit_contact_view(request, contact_id):
    """Edit an existing contact belonging to the logged-in user."""
    contact = get_object_or_404(
        Contact, id=contact_id, customer__usercustomer__user=request.user
    )

    if request.method == "POST":
        form = GiftACanForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Contact updated successfully.",
                extra_tags="contact",
            )
        else:
            messages.error(request, "Failed to update contact.")

    request.session["profile_active_tab"] = "contacts"
    return redirect("profile")


@login_required
def delete_contact_view(request, contact_id):
    """Delete a contact belonging to the logged-in user."""
    contact = get_object_or_404(
        Contact, id=contact_id, customer__usercustomer__user=request.user
    )
    contact.delete()
    messages.success(
        request, "Contact deleted successfully.", extra_tags="contact"
    )
    request.session["profile_active_tab"] = "contacts"
    return redirect("profile")


# TODO: Remove before deployment
@login_required
def preview_confirmation_signup_email(request):
    """Render the real account-confirmation email in the browser, for
    styling work. Store-owner only. Uses the logged-in user's own data and
    a dummy activation link, since previewing shouldn't create a real key.
    """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    context = {
        "user": request.user,
        "activate_url": request.build_absolute_uri(
            reverse("account_confirm_email", args=["preview-key"])
        ),
        **build_email_font_urls(request),
    }
    html_body = render_to_string(
        "account/email/email_confirmation_signup_message.html", context
    )
    return HttpResponse(html_body)


# TODO: Remove before deployment
@login_required
def preview_account_already_exists_email(request):
    """Render the real account-already-exists email in the browser, for
    styling work. Store-owner only. Uses the logged-in user's own email and
    a dummy reset link, since previewing shouldn't create a real one.
    """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    context = {
        "email": request.user.email,
        "password_reset_url": request.build_absolute_uri(
            reverse("account_reset_password")
        ),
        **build_email_font_urls(request),
    }
    html_body = render_to_string(
        "account/email/account_already_exists_message.html", context
    )
    return HttpResponse(html_body)


# TODO: Remove before deployment
@login_required
def preview_password_reset_email(request):
    """Render the real password-reset email in the browser, for styling
    work. Store-owner only. Builds a genuine reset key for the logged-in
    user the same way allauth does, so the button in the preview actually
    works and lands on the "set a new password" page.
    """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, only store owners can do that.")
        return redirect(reverse("home"))

    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import user_pk_to_url_str

    token_generator = allauth_settings.PASSWORD_RESET_TOKEN_GENERATOR()
    key = "{}-{}".format(
        user_pk_to_url_str(request.user),
        token_generator.make_token(request.user),
    )

    context = {
        "user": request.user,
        "password_reset_url": get_adapter(
            request
        ).get_reset_password_from_key_url(key),
        **build_email_font_urls(request),
    }
    html_body = render_to_string(
        "account/email/password_reset_key_message.html", context
    )
    return HttpResponse(html_body)
