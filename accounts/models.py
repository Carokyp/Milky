from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)
    iso_code = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name


class Customer(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} {self.surname}"


class UserCustomer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.customer}"


class Contact(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.name} {self.surname}"
