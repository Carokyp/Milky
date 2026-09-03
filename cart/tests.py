"""Tests for the cart app: the session-based cart operations and the
cart-totals context processor.

Run with:  python manage.py test cart
"""

from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from products.tests import make_product


class AddToCartTests(TestCase):
    def setUp(self):
        self.product = make_product(price=Decimal("4.00"))

    def _add(self, quantity):
        return self.client.post(
            reverse("add_to_cart", args=[self.product.id]),
            {"quantity": quantity, "redirect_url": "/"},
        )

    def test_adding_a_product_puts_it_in_the_session_cart(self):
        self._add(2)
        self.assertEqual(
            self.client.session["cart"], {str(self.product.id): 2}
        )

    def test_adding_again_increases_the_quantity(self):
        self._add(2)
        self._add(3)
        self.assertEqual(self.client.session["cart"][str(self.product.id)], 5)

    def test_quantity_is_capped_at_99(self):
        self._add(90)
        self._add(50)
        self.assertEqual(self.client.session["cart"][str(self.product.id)], 99)

    def test_an_unavailable_product_cannot_be_added(self):
        self.product.is_available = False
        self.product.save()
        self._add(1)
        self.assertNotIn("cart", self.client.session)


class UpdateAndRemoveTests(TestCase):
    def setUp(self):
        self.product = make_product()
        session = self.client.session
        session["cart"] = {str(self.product.id): 5}
        session.save()

    def test_update_sets_the_exact_quantity(self):
        self.client.post(
            reverse("update_cart", args=[self.product.id]), {"quantity": 2}
        )
        self.assertEqual(self.client.session["cart"][str(self.product.id)], 2)

    def test_update_never_goes_below_1(self):
        self.client.post(
            reverse("update_cart", args=[self.product.id]), {"quantity": 0}
        )
        self.assertEqual(self.client.session["cart"][str(self.product.id)], 1)

    def test_remove_deletes_the_line(self):
        self.client.post(reverse("remove_from_cart", args=[self.product.id]))
        self.assertEqual(self.client.session["cart"], {})


class CartTotalsContextTests(TestCase):
    """cart_contents() feeds every template the running totals."""

    def setUp(self):
        self.product = make_product(price=Decimal("10.00"))

    def test_totals_below_free_delivery_threshold(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): 2}  # 20.00
        session.save()

        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.context["total"], Decimal("20.00"))
        self.assertEqual(response.context["delivery"], Decimal("3.99"))
        self.assertEqual(response.context["grand_total"], Decimal("23.99"))
        self.assertEqual(
            response.context["remaining_for_free_delivery"], Decimal("5.00")
        )

    def test_delivery_becomes_free_over_the_threshold(self):
        session = self.client.session
        session["cart"] = {str(self.product.id): 3}  # 30.00
        session.save()

        response = self.client.get(reverse("view_cart"))
        self.assertEqual(response.context["delivery"], Decimal("0.00"))
        self.assertEqual(response.context["grand_total"], Decimal("30.00"))


class GiftInCartTests(TestCase):
    """A gift in the session adds the 10% promo discount and can be removed."""

    def setUp(self):
        self.product = make_product(price=Decimal("10.00"))
        session = self.client.session
        session["gift"] = {
            "product_id": str(self.product.id),
            "contact_id": 999,  # may not exist; the discount still applies
            "personal_message": "",
        }
        session.save()

    def test_gift_applies_the_10_percent_discount(self):
        response = self.client.get(reverse("view_cart"))
        # 10.00 gift + 3.99 delivery = 13.99, then 10% off -> 12.59
        self.assertEqual(response.context["promo_discount"], Decimal("10"))
        self.assertEqual(response.context["grand_total"], Decimal("12.59"))

    def test_remove_gift_frees_the_slot(self):
        self.client.post(reverse("remove_gift"))
        self.assertNotIn("gift", self.client.session)
