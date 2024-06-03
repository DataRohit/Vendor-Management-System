# Imports
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


# Define the URL patterns for the Django project
urlpatterns = [
    # Admin URL pattern, defined by the ADMIN_URL setting
    path(settings.ADMIN_URL, admin.site.urls),
    # Core App URL patterns
    path("", include("vendor_management_system.core.urls")),
    # Vendor App URL patterns
    path("vendors/", include("vendor_management_system.vendors.urls")),
    # User App URL patterns
    path("users/", include("vendor_management_system.users.urls")),
    # Purchase Orders App URL patterns
    path("purchase-orders/", include("vendor_management_system.purchase_orders.urls")),
]


# Swagger settings
schema_view = get_schema_view(
    openapi.Info(
        title="Vendor Management System API",
        default_version="v1",
        description="**Vendor Management System: Django / Django Rest Framework based Vendor Management System.**",
        contact=openapi.Contact(email="rohit.vilas.ingole@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


# Swagger URL pattern
urlpatterns += [
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="swagger--schema",
    ),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger--playground",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="swagger--redoc",
    ),
]
