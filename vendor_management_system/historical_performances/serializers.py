# Imports
from rest_framework.serializers import ModelSerializer

from vendor_management_system.historical_performances.models import (
    HistoricalPerformance,
)
from vendor_management_system.vendors.models import Vendor


# Serializer for Vendor
class HistoricalPerformanceVendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "vendor_code",
            "name",
        ]


# Serializer for HistoricalPerformance
class HistoricalPerformanceSerializer(ModelSerializer):
    vendor = HistoricalPerformanceVendorSerializer()

    class Meta:
        model = HistoricalPerformance
        fields = [
            "id",
            "vendor",
            "date",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]
