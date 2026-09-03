"""Tests for the accounts app: the profile / contact views, their login
gate and their per-owner scoping.

Run with:  python manage.py test accounts
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Contact, Customer, UserCustomer


class CustomerModelTests(TestCase):
    def test_str_is_the_full_name(self):
        customer = Customer.objects.create(name="Grace", surname="Hopper")
        self.assertEqual(str(customer), "Grace Hopper")


class ProfileAccessTests(TestCase):
    def test_profile_requires_login(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_logged_in_user_sees_their_profile(self):
        User.objects.create_user("mel", password="pw-123456")
        self.client.login(username="mel", password="pw-123456")
        self.assertEqual(self.client.get(reverse("profile")).status_code, 200)


class AddContactTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("mel", password="pw-123456")
        self.client.login(username="mel", password="pw-123456")

    def test_a_contact_needs_a_completed_profile_first(self):
        # No Customer linked yet -> the view bounces back to the profile.
        response = self.client.post(reverse("add_contact"), {})
        self.assertRedirects(response, reverse("profile"))
        self.assertEqual(Contact.objects.count(), 0)

    def test_contact_is_created_once_a_profile_exists(self):
        customer = Customer.objects.create(name="Mel", surname="B")
        UserCustomer.objects.create(user=self.user, customer=customer)

        self.client.post(
            reverse("add_contact"),
            {
                "name": "Pat",
                "surname": "Friend",
                "email": "pat@example.com",
                "phone_number": "0123456789",
                "address": "2 Friend Road",
                "city": "Leeds",
                "postal_code": "LS1 1AA",
                "country": "GB",
            },
        )
        self.assertEqual(customer.contact_set.count(), 1)


class ContactOwnershipTests(TestCase):
    """One user must not be able to touch another user's contact."""

    def setUp(self):
        owner = User.objects.create_user("owner", password="pw-123456")
        self.customer = Customer.objects.create(name="Owner", surname="One")
        UserCustomer.objects.create(user=owner, customer=self.customer)
        self.contact = Contact.objects.create(
            customer=self.customer,
            name="Pat",
            surname="Friend",
            email="pat@example.com",
            phone_number="0123456789",
            address="2 Friend Road",
            city="Leeds",
            postal_code="LS1 1AA",
            country="GB",
            ip_address="127.0.0.1",
        )
        User.objects.create_user("intruder", password="pw-123456")
        self.client.login(username="intruder", password="pw-123456")

    def test_another_user_cannot_delete_the_contact(self):
        response = self.client.post(
            reverse("delete_contact", args=[self.contact.id])
        )
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Contact.objects.filter(id=self.contact.id).exists())

    def test_another_user_cannot_edit_the_contact(self):
        response = self.client.post(
            reverse("edit_contact", args=[self.contact.id]),
            {"name": "Hacked"},
        )
        self.assertEqual(response.status_code, 404)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Pat")
