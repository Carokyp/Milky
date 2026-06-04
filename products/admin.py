from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "flavor", "sku", "price", "stock", "product_image")
    ordering = ("sku",)
    list_filter = ("is_available",)


admin.site.register(Product, ProductAdmin)
