from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserCustomer
from .forms import CustomerForm


@login_required
def profile_view(request):
    """View for the user profile page."""

    user_customers = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customers.customer if user_customers else None

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            if not user_customers:
                # Create a new UserCustomer if it doesn't exist
                UserCustomer.objects.create(user=request.user, customer=form.instance)
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        # Handle GET request to display the profile page
        form = CustomerForm(instance=customer)

    context = {
        'user_customers': user_customers,
        'customer': customer,
        'form': form,
    }

    return render(request, "accounts/profile.html", context)
