from django.contrib import admin

from accounts.models import UserCustomer
from .models import Product, Review


class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for the Product model."""

    list_display = (
        "name",
        "flavor",
        "sku",
        "price",
        "stock",
        "product_image",
    )
    ordering = ("sku",)
    list_filter = ("is_available", "flavor")


class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for the Review model."""

    list_display = (
        "name",
        "surname",
        "get_username",
        "product",
        "star_display",
        "short_comment",
    )
    ordering = ("-rating",)
    list_filter = ("rating", "product")
    search_fields = ("name", "surname", "product__name")

    def get_queryset(self, request):
        """Prefetch order and customer to avoid extra queries."""
        return super().get_queryset(request).select_related("order__customer")

    @admin.display(description="Rating")
    def star_display(self, obj):
        """Return the rating as star characters."""
        return "★" * obj.rating + "☆" * (5 - obj.rating)

    @admin.display(description="Comment")
    def short_comment(self, obj):
        """Return the comment, truncated to 60 characters."""
        if not obj.comment:
            return "—"
        if len(obj.comment) > 60:
            return obj.comment[:60] + "…"
        return obj.comment

    @admin.display(description="Username")
    def get_username(self, obj):
        """Return the username for the review's order, if any."""
        if not obj.order or not obj.order.customer:
            return "—"
        uc = UserCustomer.objects.filter(customer=obj.order.customer).first()
        return uc.user.username if uc else "—"


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
