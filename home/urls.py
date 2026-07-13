from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    
    # TODO: Remove test URLs before deployment
    path("test-success/", views.test_success, name="test_success"),
    path("test-warning/", views.test_warning, name="test_warning"),
    path("test-error/", views.test_error, name="test_error"),
    path("test-info/", views.test_info, name="test_info"),
    path("test-404/", views.test_404, name="test_404"),
    path("test-403/", views.test_403, name="test_403"),
    path("test-405/", views.test_405, name="test_405"),
    path("test-500/", views.test_500, name="test_500"),
]
