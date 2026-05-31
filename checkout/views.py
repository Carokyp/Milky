import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse

from accounts.models import UserCustomer
from cart.context_processors import cart_contents

from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product

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
                'invoice_name': form.cleaned_data.get('invoice_name', ''),
                'invoice_surname': form.cleaned_data.get('invoice_surname', ''),
                'invoice_phone': form.cleaned_data.get('invoice_phone', ''),
                'invoice_address': form.cleaned_data.get('invoice_address', ''),
                'invoice_city': form.cleaned_data.get('invoice_city', ''),
                'invoice_county': form.cleaned_data.get('invoice_county', ''),
                'invoice_postcode': form.cleaned_data.get('invoice_postcode', ''),
                'invoice_country': str(form.cleaned_data.get('invoice_country', '')),
            }
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error'}, status=400)

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


@login_required
def checkout_success(request):
    order_data = request.session.get('order_data', {})
    cart = request.session.get('cart', {})

    if not order_data or not cart:
        messages.error(request, 'Something went wrong. Please try again.')
        return redirect(reverse('checkout'))

    user_customers = UserCustomer.objects.filter(user=request.user).first()
    customer = user_customers.customer if user_customers else None

    same_as_delivery = order_data.get('same_as_delivery', True)

    order = Order(
        customer=customer,
        delivery_name=order_data['delivery_name'],
        delivery_surname=order_data['delivery_surname'],
        delivery_phone=order_data['delivery_phone'],
        delivery_address=order_data['delivery_address'],
        delivery_city=order_data['delivery_city'],
        delivery_county=order_data.get('delivery_county', ''),
        delivery_postcode=order_data.get('delivery_postcode', ''),
        delivery_country=order_data['delivery_country'],
        invoice_name=order_data['delivery_name'] if same_as_delivery else order_data.get('invoice_name', ''),
        invoice_surname=order_data['delivery_surname'] if same_as_delivery else order_data.get('invoice_surname', ''),
        invoice_phone=order_data['delivery_phone'] if same_as_delivery else order_data.get('invoice_phone', ''),
        invoice_address=order_data['delivery_address'] if same_as_delivery else order_data.get('invoice_address', ''),
        invoice_city=order_data['delivery_city'] if same_as_delivery else order_data.get('invoice_city', ''),
        invoice_county=order_data.get('delivery_county', '') if same_as_delivery else order_data.get('invoice_county', ''),
        invoice_postcode=order_data.get('delivery_postcode', '') if same_as_delivery else order_data.get('invoice_postcode', ''),
        invoice_country=order_data['delivery_country'] if same_as_delivery else order_data.get('invoice_country', ''),
    )

    cart_data = cart_contents(request)
    order.order_total = cart_data['total']
    order.delivery_cost = cart_data['delivery']
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
            messages.error(request, 'Product not found.')
            order.delete()
            return redirect(reverse('cart'))

    # Clear session
    del request.session['cart']
    del request.session['order_data']

    messages.success(
        request,
        f'Order {order.reference_code} placed successfully! You will receive a confirmation email at {request.user.email} shortly.'
    )

    return redirect(reverse('order_confirmation', args=[order.reference_code]))


@login_required
def order_confirmation(request, reference_code):
    order = get_object_or_404(Order, reference_code=reference_code, customer__usercustomer__user=request.user)
    return render(request, 'checkout/checkout_success.html', {'order': order})
