from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import OrderForm
from accounts.models import UserCustomer
from cart.context_processors import cart_contents


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

    return render(request, 'checkout/checkout.html', {'form': order_form})
