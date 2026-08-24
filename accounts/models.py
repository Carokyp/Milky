from django.db import models
from django_countries.fields import CountryField


class Customer(models.Model):
    """Delivery/contact profile linked to a user via UserCustomer."""

    # Personal info
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)

    # Address
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    county = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField(null=True, blank=True)

    def __str__(self):
        """Return the customer's full name."""
        return f"{self.name} {self.surname}"


class UserCustomer(models.Model):
    """Link between a Django user account and its Customer profile."""

    # Relationships
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        """Return the linked username and customer."""
        return f"{self.user.username} - {self.customer}"


class Contact(models.Model):
    """A person a customer can gift a can to."""

    # Relationship
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # Personal info
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    # Technical
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        """Return the contact's full name."""
        return f"{self.name} {self.surname}"
