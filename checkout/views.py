import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.models import UserCustomer
from cart.context_processors import cart_contents

from .forms import OrderForm

stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required
def checkout(request):

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty.')
        return redirect(reverse('products'))

    user_customers = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customers.customer if user_customers else None

    if not customer:
        messages.warning(request, 'Please complete your profile before checkout.')
        return redirect(reverse('profile'))

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

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save form data to session
            same_as_delivery = request.POST.get('same-as-delivery')
            request.session['order_data'] = {
                'delivery_name': form.cleaned_data['delivery_name'],
                'delivery_surname': form.cleaned_data['delivery_surname'],
                'delivery_phone': form.cleaned_data['delivery_phone'],
                'delivery_address': form.cleaned_data['delivery_address'],
                'delivery_city': form.cleaned_data['delivery_city'],
                'delivery_county': form.cleaned_data.get('delivery_county', ''),
                'delivery_postcode': form.cleaned_data.get('delivery_postcode', ''),
                'delivery_country': str(form.cleaned_data['delivery_country']),
                'same_as_delivery': bool(same_as_delivery),
           
                # Invoice fields
                'invoice_name': form.cleaned_data.get('invoice_name', ''),
                'invoice_surname': form.cleaned_data.get('invoice_surname', ''),
                'invoice_phone': form.cleaned_data.get('invoice_phone', ''),
                'invoice_address': form.cleaned_data.get('invoice_address', ''),
                'invoice_city': form.cleaned_data.get('invoice_city', ''),
                'invoice_county': form.cleaned_data.get('invoice_county', ''),
                'invoice_postcode': form.cleaned_data.get('invoice_postcode', ''),
                'invoice_country': str(form.cleaned_data.get('invoice_country', '')),
            }
        else:
            order_form = form

    cart_data = cart_contents(request)

    payment_intent = stripe.PaymentIntent.create(
        amount=int(cart_data['grand_total'] * 100),
        currency='usd',
        metadata={'user_id': request.user.id}
    )

    return render(request, 'checkout/checkout.html', {
        'form': order_form,
        'client_secret': payment_intent.client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })
