# Imports
from django.contrib import admin

from vendor_management_system.purchase_orders.models import PurchaseOrder


# Register PurchaseOrder model in admin
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = [
        "po_number",
        "vendor",
        "order_date",
        "expected_delivery_date",
        "status",
    ]
    search_fields = ["po_number", "vendor__name"]
    ordering = ["order_date"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "po_number",
                    "vendor",
                    "status",
                    "quality_rating",
                )
            },
        ),
        (
            "Dates",
            {
                "fields": (
                    "order_date",
                    "issue_date",
                    "acknowledgment_date",
                    "expected_delivery_date",
                    "actual_delivery_date",
                )
            },
        ),
        (
            "Items",
            {
                "fields": (
                    "items",
                    "quantity",
                )
            },
        ),
    )
    readonly_fields = [
        "po_number",
        # "vendor",
        # "order_date",
        # "issue_date",
        # "acknowledgment_date",
        # "expected_delivery_date",
        # "actual_delivery_date",
    ]
    ordering = ["order_date"]
    list_filter = ["status"]
