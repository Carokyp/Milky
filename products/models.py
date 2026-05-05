from django.db import models


class Product(models.Model):

    name = models.CharField(max_length=255)
    flavor = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    product_image_url = models.URLField(null=True, blank=True)
    stock = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
