# Imports
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError

from vendor_management_system.purchase_orders.models import PurchaseOrder
from vendor_management_system.vendors.models import Vendor


# Serializer for Vendor
class PurchaseOrderVendorSerializer(ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            "vendor_code",
            "name",
        ]


# Serializer for PurchaseOrder
class PurchaseOrderSerializer(ModelSerializer):
    vendor = PurchaseOrderVendorSerializer()

    class Meta:
        model = PurchaseOrder
        fields = [
            "po_number",
            "vendor",
            "order_date",
            "expected_delivery_date",
            "actual_delivery_date",
            "items",
            "quantity",
            "status",
            "quality_rating",
            "issue_date",
            "acknowledgment_date",
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

    # Method to create a new PurchaseOrder instance
    def create(self, validated_data):
        # Remove the items list
        items = validated_data.pop("items")

        # Create a new PurchaseOrder instance
        purchase_order = PurchaseOrder.objects.create(**validated_data)

        # Update the items
        purchase_order.items = items

        # Save the PurchaseOrder instance
        purchase_order.save()

        # Return the PurchaseOrder instance
        return purchase_order


# Serializer for PurchaseOrder List
class PurchaseOrderListSerializer(ModelSerializer):
    vendor = PurchaseOrderVendorSerializer()

    class Meta:
        model = PurchaseOrder
        fields = [
            "po_number",
            "vendor",
            "order_date",
            "expected_delivery_date",
            "quantity",
            "status",
            "quality_rating",
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


# Serializer for PurchaseOrder Item
class PurchaseOrderItemSerializer(serializers.Serializer):
    item = serializers.CharField()
    quantity = serializers.IntegerField()

    # Method to validate the data
    def to_internal_value(self, data):
        # Set the allowed fields
        allowed_fields = {"item", "quantity"}

        # Dict to store the errors
        errors = {}

        # Traverse over the data fields
        for field in data:
            # If field not valid, add to errors
            if field not in allowed_fields:
                errors[field] = "This field is not allowed."

        # If errors, raise validation error
        if errors:
            raise ValidationError(errors)

        # Return the validated data
        return super().to_internal_value(data)


# Serializer for PurchaseOrder Create/Update
class PurchaseOrderCreateUpdateSerializer(ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            "order_date",
            "expected_delivery_date",
            "items",
        ]

    # Method to validate the data
    def validate(self, data):
        # Get the list of allowed fields
        allowed_fields = set(self.Meta.fields)

        # Get the list of fields provided in the input data
        received_fields = set(self.initial_data.keys())

        # Get the extra fields
        extra_fields = received_fields - allowed_fields

        # If there are extra fields, raise a validation error
        if extra_fields:
            raise ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )

        # Return the validated data
        return data


# Serializer for PurchaseOrder Issue/Acknowledge
class PurchaseOrderOnlyVendorSerializer(ModelSerializer):
    vendor = serializers.CharField()

    class Meta:
        model = PurchaseOrder
        fields = ["vendor"]

    # Method to validate the data
    def validate(self, data):
        # Get the list of allowed fields
        allowed_fields = set(self.Meta.fields)

        # Get the list of fields provided in the input data
        received_fields = set(self.initial_data.keys())

        # Get the extra fields
        extra_fields = received_fields - allowed_fields

        # If there are extra fields, raise a validation error
        if extra_fields:
            raise ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )

        # Return the validated data
        return data


# Serializer for PurchaseOrder Quality Rating
class PurchaseOrderSetQualityRatingSerializer(ModelSerializer):
    vendor = serializers.CharField()
    quality_rating = serializers.IntegerField()

    class Meta:
        model = PurchaseOrder
        fields = ["vendor", "quality_rating"]

    # Method to validate the data
    def validate(self, data):
        # Get the list of allowed fields
        allowed_fields = set(self.Meta.fields)

        # Get the list of fields provided in the input data
        received_fields = set(self.initial_data.keys())

        # Get the extra fields
        extra_fields = received_fields - allowed_fields

        # If there are extra fields, raise a validation error
        if extra_fields:
            raise ValidationError(
                {field: "This field is not allowed." for field in extra_fields}
            )

        # Return the validated data
        return data
