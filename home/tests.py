"""Tests for the home app: the landing page and its featured-products
showcase.

Run with:  python manage.py test home
"""

from django.test import TestCase
from django.urls import reverse

from products.tests import make_product


class HomePageTests(TestCase):
    def setUp(self):
        self.featured = make_product(name="Featured can", featured=True)
        self.plain = make_product(name="Plain can", featured=False)
        self.featured_hidden = make_product(
            name="Featured but hidden", featured=True, is_available=False
        )

    def test_home_page_loads(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_showcase_only_shows_featured_and_available_products(self):
        response = self.client.get(reverse("home"))
        names = [p.name for p in response.context["products"]]
        self.assertEqual(names, ["Featured can"])
