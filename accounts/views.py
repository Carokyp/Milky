from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from checkout.models import Order

from .forms import CustomerForm, GiftACanForm
from .models import Contact, UserCustomer


@login_required
def profile_view(request):
    """Display and update the logged-in user's customer profile."""
    user_customers = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customers.customer if user_customers else None
    orders = Order.objects.filter(customer=customer) if customer else None
    contacts = customer.contact_set.all() if customer else []  # type: ignore
    contact_form = GiftACanForm()
    active_tab = request.session.pop('profile_active_tab', 'profile')

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
        customer__usercustomer__user=request.user
    )
    return render(request, 'checkout/checkout_success.html', {
        'order': order,
        'from_profile': True,
    })


@login_required
def add_contact_view(request):
    """Add a new contact for the logged-in user's customer profile."""
    user_customer = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customer.customer if user_customer else None

    if not customer:
        messages.error(request, 'Please complete your profile first.')
        return redirect('profile')

    if request.method == 'POST':
        form = GiftACanForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.customer = customer
            contact.ip_address = request.META.get('REMOTE_ADDR', '')
            contact.save()
            messages.success(
                request, 'Contact added successfully.', extra_tags="contact"
            )
        else:
            messages.error(request, 'Failed to add contact.')

    request.session['profile_active_tab'] = 'contacts'
    return redirect('profile')


@login_required
def edit_contact_view(request, contact_id):
    """Edit an existing contact belonging to the logged-in user."""
    contact = get_object_or_404(
        Contact, id=contact_id, customer__usercustomer__user=request.user
    )

    if request.method == 'POST':
        form = GiftACanForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Contact updated successfully.',
                extra_tags="contact",
            )
        else:
            messages.error(request, 'Failed to update contact.')

    request.session['profile_active_tab'] = 'contacts'
    return redirect('profile')


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
    request.session['profile_active_tab'] = 'contacts'
    return redirect('profile')


def handler404(request, exception):
    """Render the custom 404 error page."""
    return render(request, 'errors/404.html', status=404)


def handler403(request, exception):
    """Render the custom 403 error page."""
    return render(request, 'errors/403.html', status=403)


def handler405(request, exception):
    """Render the custom 405 error page."""
    return render(request, 'errors/405.html', status=405)


def handler500(request):
    """Render the custom 500 error page."""
    return render(request, 'errors/500.html', status=500)
