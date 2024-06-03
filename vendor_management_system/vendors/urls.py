# Imports
from django.urls import path

from vendor_management_system.vendors.views import VendorViewSet


# Define the URL patterns for the vendors app
urlpatterns = [
    path(
        "",
        VendorViewSet.as_view({"get": "list", "post": "create"}),
        name="vendors--list-create-vendor",
    ),
    path(
        "<vendor_code>/",
        VendorViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
