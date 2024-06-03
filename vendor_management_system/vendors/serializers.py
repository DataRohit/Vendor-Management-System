# Imports
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from vendor_management_system.vendors.models import Vendor


# Serializer for Vendor
class VendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "vendor_code",
            "name",
            "contact_details",
            "address",
            "on_time_delivery_rate",
            "quality_rating_avg",
            "average_response_time",
            "fulfillment_rate",
        ]

    # Method to validate the data
    def validate(self, data):
        # Get the list of allowed fields from the Meta class
        allowed_fields = set(self.Meta.fields)

        # Get the list of fields provided in the input data
        received_fields = set(self.initial_data.keys())

        # Calculate the extra fields by subtracting allowed fields from received fields
        extra_fields = received_fields - allowed_fields

        # If there are extra fields, raise a validation error
        if extra_fields:
            raise ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )

        # Return the validated data
        return data


# Serializer for PurchaseOrder Create/Update
class VendorCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "name",
            "contact_details",
            "address",
        ]

    # Method to validate the data
    def validate(self, data):
        # Get the list of allowed fields from the Meta class
        allowed_fields = set(self.Meta.fields)

        # Get the list of fields provided in the input data
        received_fields = set(self.initial_data.keys())

        # Calculate the extra fields by subtracting allowed fields from received fields
        extra_fields = received_fields - allowed_fields

        # If there are extra fields, raise a validation error
        if extra_fields:
            raise ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )

        # Return the validated data
        return data
