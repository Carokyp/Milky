from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomerForm
from accounts.models import UserCustomer


@login_required
def checkout(request):

    user_customers = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customers.customer if user_customers else None
    form = CustomerForm(instance=customer)

    return render(request, 'checkout/checkout.html', {'form': form})
