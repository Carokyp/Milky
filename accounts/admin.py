from django.contrib import admin
from .models import Customer, UserCustomer, Contact

# Register your models here.

admin.site.register(Customer)
admin.site.register(UserCustomer)
admin.site.register(Contact)
