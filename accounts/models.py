from django.db import models
from django_countries.fields import CountryField


class Customer(models.Model):
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
        return f"{self.name} {self.surname}"


class UserCustomer(models.Model):
    # Relationships
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # Status
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.customer}"


class Contact(models.Model):
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
        return f"{self.name} {self.surname}"
