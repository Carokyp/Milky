"""Tests for the checkout app: Order / OrderItem money logic and the
order-confirmation access rules.

Run with:  python manage.py test checkout
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Customer, UserCustomer
from products.models import Product

from .models import Order, OrderItem
from .order_utils import build_order_kwargs


def make_order(**overrides):
    """Create a valid Order, letting a test override single fields.

    Order has no defaults for the delivery block or order_total, so every
    test would otherwise repeat the same long list of required fields.
    """
    data = {
        "order_total": Decimal("0.00"),
        "delivery_name": "Ada",
        "delivery_surname": "Lovelace",
        "delivery_phone": "0123456789",
        "delivery_address": "1 Analytical Engine Way",
        "delivery_city": "London",
        "delivery_country": "GB",
        "email": "ada@example.com",
    }
    data.update(overrides)
    return Order.objects.create(**data)


class OrderTotalsTests(TestCase):
    """The stored totals and the computed grand_total property."""

    def test_delivery_is_charged_below_the_free_threshold(self):
        # 20.00 is under the 25.00 free-delivery threshold, so the 3.99
        # fee applies. delivery_cost is recomputed inside Order.save().
        order = make_order(order_total=Decimal("20.00"))
        self.assertEqual(order.delivery_cost, Decimal("3.99"))

    def test_delivery_is_free_at_or_above_the_threshold(self):
        order = make_order(order_total=Decimal("30.00"))
        self.assertEqual(order.delivery_cost, Decimal("0.00"))

    def test_empty_order_has_no_delivery_cost(self):
        # A zero subtotal means "no items", which should not be charged
        # the standard delivery fee.
        order = make_order(order_total=Decimal("0.00"))
        self.assertEqual(order.delivery_cost, Decimal("0.00"))

    def test_grand_total_is_subtotal_plus_delivery(self):
        order = make_order(order_total=Decimal("20.00"))
        # 20.00 + 3.99 delivery
        self.assertEqual(order.grand_total, Decimal("23.99"))

    def test_grand_total_applies_the_gift_promo_discount(self):
        order = make_order(
            order_total=Decimal("20.00"),
            promo_discount_percent=Decimal("10.00"),
        )
        # (20.00 + 3.99) * 0.90 = 21.591 -> rounded to 21.59
        self.assertEqual(order.grand_total, Decimal("21.59"))

    def test_reference_code_is_generated_and_unique(self):
        first = make_order()
        second = make_order()
        self.assertTrue(first.reference_code.startswith("ORDER-"))
        self.assertNotEqual(first.reference_code, second.reference_code)


class OrderItemSyncTests(TestCase):
    """Saving an OrderItem keeps its line total and the order total in sync."""

    def setUp(self):
        self.product = Product.objects.create(
            name="Choc Shake",
            description="Rich chocolate milkshake in a can.",
            price=Decimal("5.00"),
        )
        self.order = make_order(order_total=Decimal("0.00"))

    def test_line_total_is_quantity_times_unit_price(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            sku=self.product.sku,
            unit_price=Decimal("5.00"),
            quantity=3,
            total_price=Decimal("0.00"),  # deliberately wrong, save() fixes it
        )
        self.assertEqual(item.total_price, Decimal("15.00"))

    def test_saving_an_item_refreshes_the_parent_order_total(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            unit_price=Decimal("5.00"),
            quantity=3,
            total_price=Decimal("15.00"),
        )
        self.order.refresh_from_db()
        self.assertEqual(self.order.order_total, Decimal("15.00"))
        # 15.00 is under the threshold, so delivery is now charged too.
        self.assertEqual(self.order.delivery_cost, Decimal("3.99"))


class OrderConfirmationAccessTests(TestCase):
    """A signed-in user may only view their own order confirmation."""

    def setUp(self):
        self.owner = User.objects.create_user("owner", password="pw-123456")
        self.other = User.objects.create_user("other", password="pw-123456")

        customer = Customer.objects.create(name="Owner", surname="One")
        UserCustomer.objects.create(user=self.owner, customer=customer)
        self.order = make_order(customer=customer)

    def test_owner_can_open_their_confirmation(self):
        self.client.force_login(self.owner)
        url = reverse("order_confirmation", args=[self.order.reference_code])
        self.assertEqual(self.client.get(url).status_code, 200)

    def test_another_user_gets_404(self):
        self.client.force_login(self.other)
        url = reverse("order_confirmation", args=[self.order.reference_code])
        self.assertEqual(self.client.get(url).status_code, 404)


class CheckoutGuardTests(TestCase):
    """The checkout page refuses an empty cart."""

    def test_empty_cart_redirects_to_the_catalogue(self):
        response = self.client.get(reverse("checkout"))
        self.assertRedirects(response, reverse("all_products"))


class BuildOrderKwargsTests(TestCase):
    """build_order_kwargs() shared by the checkout view and the webhook."""

    def _order_data(self, **override):
        data = {
            "same_as_delivery": True,
            "delivery_name": "Ada",
            "delivery_surname": "Lovelace",
            "delivery_city": "London",
            "email": "ada@example.com",
        }
        data.update(override)
        return data

    def test_promo_discount_is_set_only_when_there_is_a_gift(self):
        with_gift = build_order_kwargs(
            self._order_data(), customer=None, gift={"product_id": "1"}
        )
        without_gift = build_order_kwargs(
            self._order_data(), customer=None, gift=None
        )
        self.assertEqual(with_gift["promo_discount_percent"], Decimal("10"))
        self.assertIsNone(without_gift["promo_discount_percent"])

    def test_invoice_falls_back_to_delivery_when_same_as_delivery(self):
        kwargs = build_order_kwargs(
            self._order_data(), customer=None, gift=None
        )
        self.assertEqual(kwargs["invoice_name"], "Ada")
        self.assertEqual(kwargs["invoice_city"], "London")

    def test_separate_invoice_address_is_kept_when_requested(self):
        kwargs = build_order_kwargs(
            self._order_data(
                same_as_delivery=False,
                invoice_name="Charles",
                invoice_city="Bath",
            ),
            customer=None,
            gift=None,
        )
        self.assertEqual(kwargs["invoice_name"], "Charles")
        self.assertEqual(kwargs["invoice_city"], "Bath")
