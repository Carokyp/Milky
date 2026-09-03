"""Tests for the products app: the Product / Review models, the catalogue
view filtering, and the store-owner-only management views.

Run with:  python manage.py test products
"""

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from accounts.models import Contact, Customer, UserCustomer
from checkout.models import OrderItem
from checkout.tests import make_order

from .models import Product, Review, generate_sku


def make_product(**overrides):
    """Create a Product with only the three required fields filled in."""
    data = {
        "name": "Vanilla Shake",
        "description": "Smooth vanilla milkshake in a can.",
        "price": Decimal("3.50"),
    }
    data.update(overrides)
    return Product.objects.create(**data)


class ProductModelTests(TestCase):
    def test_generate_sku_format_and_uniqueness(self):
        skus = {generate_sku() for _ in range(50)}
        self.assertTrue(all(s.startswith("MILK-") for s in skus))
        self.assertTrue(all(len(s) == len("MILK-") + 6 for s in skus))
        # 50 random draws should not collide.
        self.assertEqual(len(skus), 50)

    def test_blank_sku_is_auto_filled_on_save(self):
        product = make_product()
        self.assertTrue(product.sku.startswith("MILK-"))

    def test_single_image_url_prefers_the_uploaded_image_then_the_link(self):
        # Nothing set -> empty string, so templates can fall back safely.
        product = make_product()
        self.assertEqual(product.single_image_url, "")
        # A pasted URL is used when no file is uploaded.
        product.product_image_url = "https://example.com/can.png"
        product.save()
        self.assertEqual(
            product.single_image_url, "https://example.com/can.png"
        )


class ReviewModelTests(TestCase):
    def setUp(self):
        self.product = make_product()

    def _review(self, rating):
        return Review(
            product=self.product,
            name="Sam",
            surname="Doe",
            rating=rating,
            comment="Tasty.",
        )

    def test_rating_within_1_to_5_is_valid(self):
        for rating in (1, 3, 5):
            # full_clean() runs the model validators; no error = pass.
            self._review(rating).full_clean()

    def test_rating_outside_1_to_5_is_rejected(self):
        for rating in (0, 6):
            with self.assertRaises(ValidationError):
                self._review(rating).full_clean()


class CatalogueViewTests(TestCase):
    def setUp(self):
        self.available = make_product(name="On sale")
        self.hidden = make_product(name="Hidden", is_available=False)

    def test_all_products_lists_only_available_products(self):
        response = self.client.get(reverse("all_products"))
        self.assertEqual(response.status_code, 200)
        names = [p.name for p in response.context["products"]]
        self.assertIn("On sale", names)
        self.assertNotIn("Hidden", names)

    def test_product_detail_returns_404_for_a_missing_product(self):
        response = self.client.get(reverse("product_detail", args=[999999]))
        self.assertEqual(response.status_code, 404)


class ProductManagementPermissionTests(TestCase):
    """add / edit / delete product are for store owners (superusers) only."""

    def setUp(self):
        self.product = make_product()
        self.shopper = User.objects.create_user(
            "shopper", password="pw-123456"
        )
        self.owner = User.objects.create_superuser(
            "owner", "owner@example.com", "pw-123456"
        )

    def test_anonymous_visitor_is_sent_to_login(self):
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_signed_in_shopper_is_sent_home(self):
        self.client.force_login(self.shopper)
        response = self.client.get(reverse("add_product"))
        self.assertRedirects(response, reverse("home"))

    def test_store_owner_can_open_the_add_product_form(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("add_product"))
        self.assertEqual(response.status_code, 200)


class DeleteOrderedProductTests(TestCase):
    """A product tied to a past order is hidden, never hard-deleted."""

    def setUp(self):
        self.owner = User.objects.create_superuser(
            "owner", "owner@example.com", "pw-123456"
        )
        self.product = make_product()
        order = make_order()
        OrderItem.objects.create(
            order=order,
            product=self.product,
            unit_price=self.product.price,
            quantity=1,
            total_price=self.product.price,
        )

    def test_delete_hides_the_product_instead_of_removing_it(self):
        self.client.force_login(self.owner)
        self.client.post(reverse("delete_product", args=[self.product.id]))

        self.product.refresh_from_db()  # still here...
        self.assertFalse(self.product.is_available)  # ...just hidden
        # The order line that referenced it is intact.
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_a_product_with_no_orders_is_deleted_normally(self):
        spare = make_product(name="Never ordered")
        self.client.force_login(self.owner)
        self.client.post(reverse("delete_product", args=[spare.id]))
        self.assertFalse(Product.objects.filter(id=spare.id).exists())


class AddReviewTests(TestCase):
    def setUp(self):
        self.product = make_product()

    def test_review_form_requires_login(self):
        response = self.client.post(
            reverse("add_review", args=[self.product.id]),
            {"rating": 5, "comment": "Great"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_can_leave_a_review(self):
        User.objects.create_user("sam", password="pw-123456")
        self.client.login(username="sam", password="pw-123456")
        self.client.post(
            reverse("add_review", args=[self.product.id]),
            {"rating": 4, "comment": "Nice"},
        )
        self.assertEqual(self.product.reviews.count(), 1)
        self.assertEqual(self.product.reviews.first().rating, 4)


class GiftPageTests(TestCase):
    """The Gift a Can page: who may use it and the one-gift-per-order rule."""

    def setUp(self):
        self.product = make_product()
        self.user = User.objects.create_user("gifter", password="pw-123456")
        self.customer = Customer.objects.create(name="Gift", surname="Er")
        UserCustomer.objects.create(user=self.user, customer=self.customer)

    def _new_friend_post(self, **override):
        data = {
            "product_id": self.product.id,
            "name": "Pat",
            "surname": "Friend",
            "email": "pat@example.com",
            "phone_number": "0123456789",
            "address": "3 Friend Road",
            "city": "Leeds",
            "postal_code": "LS1 1AA",
            "country": "GB",
        }
        data.update(override)
        return data

    def test_page_loads_for_a_guest(self):
        self.assertEqual(
            self.client.get(reverse("gift_page")).status_code, 200
        )

    def test_posting_while_logged_out_redirects_to_login(self):
        response = self.client.post(
            reverse("gift_page"), self._new_friend_post()
        )
        self.assertRedirects(
            response,
            reverse("account_login"),
            fetch_redirect_response=False,
        )

    def test_posting_without_a_profile_redirects_to_profile(self):
        User.objects.create_user("bare", password="pw-123456")
        self.client.login(username="bare", password="pw-123456")
        response = self.client.post(
            reverse("gift_page"), self._new_friend_post()
        )
        self.assertRedirects(response, reverse("profile"))

    def test_a_valid_gift_is_stored_in_the_session(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("gift_page"), self._new_friend_post()
        )
        self.assertRedirects(response, reverse("view_cart"))
        self.assertEqual(
            self.client.session["gift"]["product_id"], str(self.product.id)
        )
        self.assertEqual(Contact.objects.count(), 1)

    def test_only_one_gift_per_order(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["gift"] = {
            "product_id": str(self.product.id),
            "contact_id": 1,
            "personal_message": "",
        }
        session.save()

        response = self.client.post(
            reverse("gift_page"), self._new_friend_post()
        )
        self.assertRedirects(response, reverse("gift_page"))
        # The second attempt never creates a contact.
        self.assertEqual(Contact.objects.count(), 0)

    def test_gifting_an_unavailable_product_is_rejected(self):
        self.client.force_login(self.user)
        self.product.is_available = False
        self.product.save()
        response = self.client.post(
            reverse("gift_page"), self._new_friend_post()
        )
        self.assertRedirects(response, reverse("gift_page"))
        self.assertNotIn("gift", self.client.session)

    def test_gifting_to_a_saved_contact(self):
        self.client.force_login(self.user)
        contact = Contact.objects.create(
            customer=self.customer,
            name="Sam",
            surname="Saved",
            email="sam@example.com",
            phone_number="0123456789",
            address="4 Saved Street",
            city="York",
            postal_code="YO1 1AA",
            country="GB",
            ip_address="127.0.0.1",
        )
        response = self.client.post(
            reverse("gift_page"),
            {"product_id": self.product.id, "existing_contact": contact.id},
        )
        self.assertRedirects(response, reverse("view_cart"))
        self.assertEqual(self.client.session["gift"]["contact_id"], contact.id)
