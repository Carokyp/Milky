from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import OrderForm
from accounts.models import UserCustomer


@login_required
def checkout(request):

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect(reverse('products'))

    user_customers = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customers.customer if user_customers else None

    order_form = OrderForm(initial={
        'delivery_name': customer.name if customer else '',
        'delivery_surname': customer.surname if customer else '',
        'delivery_phone': customer.phone_number if customer else '',
        'delivery_address': customer.address if customer else '',
        'delivery_city': customer.city if customer else '',
        'delivery_county': customer.county if customer else '',
        'delivery_postcode': customer.postal_code if customer else '',
        'delivery_country': customer.country if customer else '',
    })

    return render(request, 'checkout/checkout.html', {'form': order_form})
