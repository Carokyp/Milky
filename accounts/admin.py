from django.contrib import admin
from .models import Country, Customer, User_customer, Contact

# Register your models here.

admin.site.register(Country)
admin.site.register(Customer)
admin.site.register(User_customer)
admin.site.register(Contact)
