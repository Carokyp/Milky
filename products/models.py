from django.db import models
import uuid


def generate_sku():
    return f"MILK-{uuid.uuid4().hex[:6].upper()}"


class Product(models.Model):
    CHOCOLATE = "chocolate"
    VANILLA = "vanilla"
    FRUITY = "fruity"
    CARAMEL = "caramel"
    NUTTY = "nutty"
    SPECIAL = "special"

    FLAVOR_CHOICES = [
        (CHOCOLATE, "Chocolate"),
        (VANILLA, "Vanilla"),
        (FRUITY, "Fruity"),
        (CARAMEL, "Caramel"),
        (NUTTY, "Nutty"),
        (SPECIAL, "Special"),
    ]

    # Identifiers
    sku = models.CharField(max_length=255, unique=True, default=generate_sku, blank=True)
    name = models.CharField(max_length=255)
    flavor = models.CharField(max_length=50, choices=FLAVOR_CHOICES, null=True, blank=True)

    # Details
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Media
    product_image = models.ImageField(
        upload_to="product_images/", null=True, blank=True
    )
    product_image_url = models.URLField(null=True, blank=True)

    # Stock
    stock = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
