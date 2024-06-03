# Imports
from django.contrib import admin

from vendor_management_system.vendors.models import Vendor


# Register Vendor model in admin
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "vendor_code"]
    search_fields = ["name", "vendor_code"]
    ordering = ["name"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "contact_details",
                    "address",
                    "vendor_code",
                )
            },
        ),
        (
            "Performance",
            {
                "fields": (
                    "on_time_delivery_rate",
                    "quality_rating_avg",
                    "average_response_time",
                    "fulfillment_rate",
                )
            },
        ),
    )
    readonly_fields = [
        "vendor_code",
        # "on_time_delivery_rate",
        # "quality_rating_avg",
        # "average_response_time",
        # "fulfillment_rate",
    ]
    ordering = ["name"]
