from decimal import Decimal

from django.contrib import admin
from django.db.models import Sum

from .models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("total_price", "unit_price", "sku")
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    readonly_fields = (
        "reference_code",
        "created_at",
        "delivery_cost",
        "order_total",
        "grand_total",
        "stripe_pid",
    )

    fieldsets = (
        (
            "Order Info",
            {
                "fields": (
                    "reference_code",
                    "customer",
                    "email",
                    "status",
                    "created_at",
                    "stripe_pid",
                )
            },
        ),
        ("Financials", {"fields": ("order_total", "delivery_cost", "grand_total")}),
        (
            "Delivery Details",
            {
                "fields": (
                    "delivery_name",
                    "delivery_surname",
                    "delivery_phone",
                    "delivery_address",
                    "delivery_city",
                    "delivery_county",
                    "delivery_postcode",
                    "delivery_country",
                )
            },
        ),
        (
            "Invoice Details",
            {
                "fields": (
                    "invoice_name",
                    "invoice_surname",
                    "invoice_phone",
                    "invoice_address",
                    "invoice_city",
                    "invoice_county",
                    "invoice_postcode",
                    "invoice_country",
                )
            },
        ),
    )

    list_display = (
        "reference_code",
        "customer_display",
        "email",
        "status",
        "created_at",
        "order_total",
        "delivery_cost",
    )
    ordering = ("-created_at",)
    list_filter = ("status", "created_at")
    search_fields = ("reference_code", "customer__name", "customer__surname")

    def save_formset(self, request, form, formset, change):
        # Prepare OrderItems in memory without saving to DB yet
        instances = formset.save(commit=False)

        # Save each OrderItem — triggers OrderItem.save()
        # which automatically recalculates total_price
        for instance in instances:
            instance.save()

        # Delete any OrderItems the admin marked for removal
        for deleted_object in formset.deleted_objects:
            deleted_object.delete()

        # Best practice — save Many-to-Many relationships if any exist
        formset.save_m2m()

        # Recalculate the order total after all changes
        # Especially needed after an OrderItem is deleted
        order = form.instance
        order.order_total = order.items.aggregate(total=Sum("total_price"))[
            "total"
        ] or Decimal("0.00")
        order.save()

    def customer_display(self, obj):
        if obj.customer:
            return f"{obj.customer.name} {obj.customer.surname}"
        return f"{obj.delivery_name} {obj.delivery_surname} (Guest)"

    customer_display.short_description = "Customer"  # type: ignore

    # custom JavaScript to show/hide invoice fields based on "same as delivery" checkbox
    class Media:
        js = ("js/admin_invoice.js",)


admin.site.register(Order, OrderAdmin)
