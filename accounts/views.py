from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserCustomer


@login_required
def profile_view(request):
    """View for the user profile page."""

    user_customers = UserCustomer.objects.filter(user=request.user)

    context = {
        'user_customers': user_customers,
    }

    return render(request, "accounts/profile.html", context)
