from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    
    # TODO: Remove test URL before deployment
    path("test-success/", views.test_success, name="test_success"),
    path("test-warning/", views.test_warning, name="test_warning"),
    path("test-error/", views.test_error, name="test_error"),
    path("test-info/", views.test_info, name="test_info"),
]
