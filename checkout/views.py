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

    # If no customer profile, redirect to profile page
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
            try:
                order = form.save(commit=False)

                same_as_delivery = request.POST.get('same-as-delivery')
                if same_as_delivery:
                    order.invoice_name = order.delivery_name
                    order.invoice_surname = order.delivery_surname
                    order.invoice_phone = order.delivery_phone
                    order.invoice_address = order.delivery_address
                    order.invoice_city = order.delivery_city
                    order.invoice_county = order.delivery_county
                    order.invoice_postcode = order.delivery_postcode
                    order.invoice_country = order.delivery_country

                order.customer = customer
                cart_data = cart_contents(request)
                order.order_total = cart_data['total']
                order.delivery_cost = cart_data['delivery']
                order.save()
                messages.success(request, 'Order placed successfully!')
                return redirect(reverse('checkout_success', args=[order.reference_code]))

            except Exception as e:
                messages.error(request, f'There was an error processing your order: {e}')
        else:
            order_form = form

    # prepare cart data for payment intent and template
    cart_data = cart_contents(request)

    # create payment intent for frontend to complete payment
    payment_intent = stripe.PaymentIntent.create(
        amount=int(cart_data['grand_total'] * 100),  # Convert to cents
        currency='usd',
        metadata={'user_id': request.user.id}
    )

    return render(request, 'checkout/checkout.html', {
        'form': order_form,
        'client_secret': payment_intent.client_secret,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })
