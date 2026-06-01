from django.urls import path
from . import views
from .webhook import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('success/', views.checkout_success, name='checkout_success'),
    path('confirmation/<str:reference_code>/', views.order_confirmation, name='order_confirmation'),
    path('webhook/', webhook, name='webhook'),
]
