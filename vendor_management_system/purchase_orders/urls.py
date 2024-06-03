# Imports
from django.urls import path

from vendor_management_system.purchase_orders.views import PurchaseOrderViewSet


# Define the URL patterns for the purchase_orders app
urlpatterns = [
    path(
        "",
        PurchaseOrderViewSet.as_view({"get": "list", "post": "create"}),
        name="purchase_orders--list-create-order",
    ),
    path(
        "<po_number>/",
        PurchaseOrderViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="purchase_orders--retrieve-update-destroy-order",
    ),
    path(
        "<po_number>/issue/",
        PurchaseOrderViewSet.as_view({"post": "issue"}),
        name="purchase_orders--issue-order",
    ),
    path(
        "<po_number>/acknowledge/",
        PurchaseOrderViewSet.as_view({"post": "acknowledge"}),
        name="purchase_orders--acknowledge-order",
    ),
    path(
        "<po_number>/deliver/",
        PurchaseOrderViewSet.as_view({"post": "deliver"}),
        name="purchase_orders--deliver-order",
    ),
    path(
        "<po_number>/cancel/",
        PurchaseOrderViewSet.as_view({"post": "cancel"}),
        name="purchase_orders--cancel-order",
    ),
    path(
        "<po_number>/rate-quality/",
        PurchaseOrderViewSet.as_view({"post": "rate_quality"}),
        name="purchase_orders--rate-quality",
    ),
]
