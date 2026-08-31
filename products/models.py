import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


def generate_sku():
    """Return a random SKU like 'MILK-A1B2C3'."""
    return f"MILK-{uuid.uuid4().hex[:6].upper()}"


class Product(models.Model):
    """A product sold in the shop, with pricing, stock and media."""

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
    sku = models.CharField(
        max_length=255, unique=True, default=generate_sku, blank=True
    )
    name = models.CharField(max_length=255)
    flavor = models.CharField(
        max_length=50, choices=FLAVOR_CHOICES, null=True, blank=True
    )

    # Details
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    # Media — legacy single image (used in detail page, cart, etc.)
    product_image = models.ImageField(
        upload_to="product_images/", null=True, blank=True
    )
    product_image_url = models.URLField(null=True, blank=True)

    # Media — home page showcase (3 animated layers)
    background_image = models.ImageField(
        upload_to="product_images/backgrounds/", null=True, blank=True
    )
    objects_image = models.ImageField(
        upload_to="product_images/objects/", null=True, blank=True
    )
    can_image = models.ImageField(
        upload_to="product_images/cans/", null=True, blank=True
    )

    # Stock
    stock = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    # Home page display
    featured = models.BooleanField(
        default=False,
        help_text="Show this product on the home page showcase",
    )
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Lower numbers appear first among featured products",
    )

    class Meta:
        ordering = ["display_order", "name"]

    @property
    def single_image_url(self):
        """Return the cart image URL: the upload, an external link, or ''."""
        if self.product_image:
            return self.product_image.url
        # Optional external link, used only when nothing is uploaded.
        return self.product_image_url or ""

    def __str__(self):
        """Return the product name for display."""
        return self.name


class Review(models.Model):
    """A customer review left on a product."""

    order = models.ForeignKey(
        "checkout.Order", on_delete=models.SET_NULL, null=True, blank=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=500, blank=True, null=True)
