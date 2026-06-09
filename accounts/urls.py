from django.urls import path
from . import views


urlpatterns = [
    path("", views.profile_view, name="profile"),
    path("order_history/<str:reference_code>/", views.orders_history_view, name="order_history"),
]
