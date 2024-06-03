# Imports
from django.contrib import admin

from vendor_management_system.historical_performances.models import (
    HistoricalPerformance,
)


# Register HistoricalPerformance model in admin
@admin.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "vendor",
        "date",
        "on_time_delivery_rate",
        "quality_rating_avg",
        "average_response_time",
        "fulfillment_rate",
    ]
    search_fields = ["id", "vendor__name"]
    ordering = ["date"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "vendor",
                    "date",
                    "on_time_delivery_rate",
                    "quality_rating_avg",
                    "average_response_time",
                    "fulfillment_rate",
                )
            },
        ),
    )
    readonly_fields = [
        "id",
        "vendor",
        "date",
        "on_time_delivery_rate",
        "quality_rating_avg",
        "average_response_time",
        "fulfillment_rate",
    ]
    ordering = ["date"]
    list_filter = ["vendor"]
