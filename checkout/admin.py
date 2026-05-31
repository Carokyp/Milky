from decimal import Decimal

from django.contrib import admin
from django.db.models import Sum

from .models import Order, OrderItem, Payment

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('total_price', 'unit_price', 'sku')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderItemInline,)
    readonly_fields = ('reference_code', 'created_at', 'delivery_cost', 'order_total', 'grand_total')

    fieldsets = (
        ('Order Info', {
            'fields': ('reference_code', 'customer', 'status', 'created_at')
        }),
        ('Financials', {
            'fields': ('order_total', 'delivery_cost', 'grand_total')
        }),
        ('Delivery Details', {
            'fields': ('delivery_name', 'delivery_surname', 'delivery_phone',
                       'delivery_address', 'delivery_city', 'delivery_county',
                       'delivery_postcode', 'delivery_country')
        }),
        ('Invoice Details', {
            'fields': ('invoice_name', 'invoice_surname', 'invoice_phone',
                       'invoice_address', 'invoice_city', 'invoice_county',
                       'invoice_postcode', 'invoice_country')
        }),
    )

    list_display = ('reference_code', 'customer', 'status', 'created_at', 'order_total', 'delivery_cost')
    ordering = ('-created_at',)
    list_filter = ('status', 'created_at')
    search_fields = ('reference_code', 'customer__name', 'customer__surname')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            instance.save()

        for deleted_object in formset.deleted_objects:
            deleted_object.delete()

        formset.save_m2m()

        order = form.instance
        order.order_total = order.items.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
        order.save()

    class Media:
        js = ('js/admin_invoice.js',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
