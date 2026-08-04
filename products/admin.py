from django.contrib import admin
from .models import Product, Review
from accounts.models import UserCustomer


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "flavor", "sku", "price", "stock", "product_image")
    ordering = ("sku",)
    list_filter = ("is_available", "flavor")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "surname", "get_username", "product", "star_display", "short_comment")
    ordering = ("-rating",)
    list_filter = ("rating", "product")
    search_fields = ("name", "surname", "product__name")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("order__customer")

    @admin.display(description="Rating")
    def star_display(self, obj):
        return "★" * obj.rating + "☆" * (5 - obj.rating)

    @admin.display(description="Comment")
    def short_comment(self, obj):
        if not obj.comment:
            return "—"
        return (obj.comment[:60] + "…") if len(obj.comment) > 60 else obj.comment

    @admin.display(description="Username")
    def get_username(self, obj):
        if not obj.order or not obj.order.customer:
            return "—"
        uc = UserCustomer.objects.filter(customer=obj.order.customer).first()
        return uc.user.username if uc else "—"


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
