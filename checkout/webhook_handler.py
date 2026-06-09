import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from decimal import Decimal
from django.http import HttpResponse
from django.contrib.auth.models import User
from accounts.models import UserCustomer
from .models import Order, OrderItem
from products.models import Product


class StripeWHHandler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        customer_email = order.email
        subject = render_to_string(
            'checkout/confirmation_email_subject.txt',
            {'order': order}
        )
        body = render_to_string(
            'checkout/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL}
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [customer_email]
        )

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}', status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        payment_intent = event.data.object

        # Convert metadata to a plain Python dict
        metadata = (
            payment_intent.metadata.to_dict()
            if hasattr(payment_intent.metadata, "to_dict")
            else (payment_intent.metadata or {})
        )

        order_data = json.loads(metadata.get("order_data", "{}"))
        cart = json.loads(metadata.get("cart", "{}"))
        user_id = metadata.get("user_id")

        # Get the user and customer
        customer = None
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user_customer = UserCustomer.objects.filter(user=user).first()
                customer = user_customer.customer if user_customer else None
            except User.DoesNotExist:
                customer = None

        # Save delivery info to profile if save_info is True ← ajoute ici
        save_info = order_data.get("save_info", False)
        if save_info and customer:
            customer.name = order_data.get("delivery_name", "")
            customer.surname = order_data.get("delivery_surname", "")
            customer.phone_number = order_data.get("delivery_phone", "")
            customer.address = order_data.get("delivery_address", "")
            customer.city = order_data.get("delivery_city", "")
            customer.county = order_data.get("delivery_county", "")
            customer.postal_code = order_data.get("delivery_postcode", "")
            customer.country = order_data.get("delivery_country", "")
            customer.save()

        same_as_delivery = order_data.get("same_as_delivery", True)

        # Check if order already exists
        order = Order.objects.filter(
            stripe_pid=payment_intent.id,
        ).first()

        if order:
            order.status = 1  # Completed
            order.save()
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order already in database',
                status=200,
            )

        # Order doesn't exist — create it
        order = None
        try:
            order = Order.objects.create(
                customer=customer,
                status=1,  # Completed
                stripe_pid=payment_intent.id,
                delivery_name=order_data.get("delivery_name", ""),
                delivery_surname=order_data.get("delivery_surname", ""),
                delivery_phone=order_data.get("delivery_phone", ""),
                delivery_address=order_data.get("delivery_address", ""),
                delivery_city=order_data.get("delivery_city", ""),
                delivery_county=order_data.get("delivery_county", ""),
                delivery_postcode=order_data.get("delivery_postcode", ""),
                delivery_country=order_data.get("delivery_country", ""),
                invoice_name=(
                    order_data.get("delivery_name", "")
                    if same_as_delivery
                    else order_data.get("invoice_name", "")
                ),
                invoice_surname=(
                    order_data.get("delivery_surname", "")
                    if same_as_delivery
                    else order_data.get("invoice_surname", "")
                ),
                invoice_phone=(
                    order_data.get("delivery_phone", "")
                    if same_as_delivery
                    else order_data.get("invoice_phone", "")
                ),
                invoice_address=(
                    order_data.get("delivery_address", "")
                    if same_as_delivery
                    else order_data.get("invoice_address", "")
                ),
                invoice_city=(
                    order_data.get("delivery_city", "")
                    if same_as_delivery
                    else order_data.get("invoice_city", "")
                ),
                invoice_county=(
                    order_data.get("delivery_county", "")
                    if same_as_delivery
                    else order_data.get("invoice_county", "")
                ),
                invoice_postcode=(
                    order_data.get("delivery_postcode", "")
                    if same_as_delivery
                    else order_data.get("invoice_postcode", "")
                ),
                invoice_country=(
                    order_data.get("delivery_country", "")
                    if same_as_delivery
                    else order_data.get("invoice_country", "")
                ),
                order_total=Decimal("0.00"),
            )

            # Create order items
            for item_id, quantity in cart.items():
                product = Product.objects.get(id=item_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    sku=product.sku,
                    unit_price=product.price,
                    quantity=quantity,
                    total_price=product.price * quantity,
                )

        except Exception as e:
            if order:
                order.delete()
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}', status=500
            )

        self._send_confirmation_email(order)

        return HttpResponse(
            content=f'Webhook received: {event["type"]} | Order created', status=200
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        payment_intent = event.data.object
        order = Order.objects.filter(stripe_pid=payment_intent.id).first()
        if order:
            order.status = 2  # Cancelled
            order.save()
        return HttpResponse(content=f'Webhook received: {event["type"]}', status=200)
