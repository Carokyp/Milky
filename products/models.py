from django.db import models


class Product(models.Model):
    # Identifiers
    sku = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    flavor = models.CharField(max_length=255, null=True, blank=True)

    # Details
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Media
    product_image = models.ImageField(
        upload_to="product_images/", null=True, blank=True
    )
    product_image_url = models.URLField(null=True, blank=True)

    # Stock
    stock = models.IntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
