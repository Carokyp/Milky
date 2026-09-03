from django.urls import path

from . import views

urlpatterns = [
    path("", views.profile_view, name="profile"),
    path(
        "order_history/<str:reference_code>/",
        views.orders_history_view,
        name="order_history",
    ),
    path("add_contact/", views.add_contact_view, name="add_contact"),
    path(
        "delete_contact/<int:contact_id>/",
        views.delete_contact_view,
        name="delete_contact",
    ),
    path(
        "edit_contact/<int:contact_id>/",
        views.edit_contact_view,
        name="edit_contact",
    ),
]
