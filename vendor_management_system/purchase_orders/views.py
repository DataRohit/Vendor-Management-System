# Imports
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, response, status, viewsets

from vendor_management_system.core.authentication import (
    QueryParameterTokenAuthentication,
)

from vendor_management_system.purchase_orders.models import PurchaseOrder
from vendor_management_system.purchase_orders.serializers import (
    PurchaseOrderCreateUpdateSerializer,
    PurchaseOrderListSerializer,
    PurchaseOrderOnlyVendorSerializer,
    PurchaseOrderSerializer,
    PurchaseOrderSetQualityRatingSerializer,
)

from vendor_management_system.vendors.models import Vendor


# Class based ViewSet for PurchaseOrder
class PurchaseOrderViewSet(viewsets.ViewSet):
    # Set the permission and authentication classes
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [QueryParameterTokenAuthentication]

    # Method to handle listing all purchase orders
    @swagger_auto_schema(
        operation_id="purchase_orders--list-orders",
        operation_description="List all purchase orders",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            )
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                "List of all purchase orders", schema=PurchaseOrderSerializer(many=True)
            ),
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders"],
    )
    def list(self, request):
        # Get all purchase orders
        orders = PurchaseOrder.objects.all()

        # Serialize the purchase orders
        serializer = PurchaseOrderListSerializer(orders, many=True)

        # Return the response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    # Method to handle new purchase order creation
    @swagger_auto_schema(
        operation_id="purchase_order--create-order",
        operation_description="Create a new purchase order",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            )
        ],
        request_body=PurchaseOrderCreateUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "The created purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders"],
    )
    def create(self, request):
        # Deserialize and validate the data
        order_create_serializer = PurchaseOrderCreateUpdateSerializer(data=request.data)

        # If the provided data is valid
        if order_create_serializer.is_valid():
            # Get the data from order_create_serializer
            order_create_serializer_data = order_create_serializer.validated_data

            # Update the quantity
            order_create_serializer_data["quantity"] = sum(
                item["quantity"] for item in order_create_serializer_data["items"]
            )

            # Create a new PurchaseOrder instance
            purchase_order = PurchaseOrder.objects.create(
                **order_create_serializer_data
            )

            # Serialize the created purchase order
            serializer = PurchaseOrderSerializer(purchase_order)

            # Return the success response
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        # Return the error response
        return response.Response(
            order_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to handle retrieving a single order
    @swagger_auto_schema(
        operation_id="vendors--retrieve-order",
        operation_description="Retrieve a specific purchase order detail",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The purchase order number for the order to retrieve",
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The retrieved purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_404_NOT_FOUND: "Purchase order not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders"],
    )
    def retrieve(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # Serialize the purchase order
        serializer = PurchaseOrderSerializer(order)

        # Return the response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    # Method to handle updating a purchase order
    @swagger_auto_schema(
        operation_id="purchase_orders--update-order",
        operation_description="Update a specific purchase order",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The po_number for the order to update",
            ),
        ],
        request_body=PurchaseOrderCreateUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The updated purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_404_NOT_FOUND: "Purchase order / Vendor not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders"],
    )
    def update(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # Deserialize and validate the data
        order_create_serializer = PurchaseOrderCreateUpdateSerializer(
            instance=order, data=request.data, partial=True
        )

        # If the provided data is valid
        if order_create_serializer.is_valid():
            # Get the validated data
            validated_data = order_create_serializer.validated_data

            # Get the vendor and serialize the data
            if "vendor" in validated_data:
                vendor = get_object_or_404(Vendor, vendor_code=validated_data["vendor"])
            else:
                vendor = order.vendor

            # Add the vendor to the validated data
            validated_data["vendor"] = vendor

            # Update the quantity
            validated_data["quantity"] = sum(
                item["quantity"] for item in validated_data["items"]
            )

            # Update the order
            order = order_create_serializer.save()

            # Serialize the updated purchase order
            serializer = PurchaseOrderSerializer(order)

            # Return the success response
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Return the error response
        return response.Response(
            order_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to handle deleting a purchase order
    @swagger_auto_schema(
        operation_id="purchase_orders--delete-order",
        operation_description="Delete a specific purchase order",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The po_number for the order to delete",
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "Purchase order deleted",
            status.HTTP_404_NOT_FOUND: "Purchase order not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders"],
    )
    def destroy(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # Delete the order
        order.delete()

        # Return the success response
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    # Method to update the purchase order and set the status to "ISSUED"
    @swagger_auto_schema(
        operation_id="purchase_orders--issue-order",
        operation_description="Issue an order to a vendor and set the status to 'ISSUED'",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The po_number for the order to update",
            ),
        ],
        request_body=PurchaseOrderOnlyVendorSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The updated purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_404_NOT_FOUND: "Purchase order / Vendor not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders Process Operations"],
    )
    def issue(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # If the order is already issued
        if order.status in ["ISSUED", "ACKNOWLEDGED", "DELIVERED", "CANCELLED"]:
            return response.Response(
                {"status": "This order is already processed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deserialize and validate the data
        issue_serializer = PurchaseOrderOnlyVendorSerializer(data=request.data)

        # If the provided data is valid
        if issue_serializer.is_valid():
            # Get the vendor and serialize the data
            vendor = get_object_or_404(
                Vendor, vendor_code=issue_serializer.validated_data["vendor"]
            )

            # Set the vendor
            order.vendor = vendor

            # Set the status to ISSUED
            order.status = "ISSUED"

            # Save the order
            order.save()

            # Serialize the updated purchase order
            serializer = PurchaseOrderSerializer(order)

            # Return the success response
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Return the error response
        return response.Response(
            issue_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to update the purchase order and set the status to "ACKNOWLEDGED"
    @swagger_auto_schema(
        operation_id="purchase_orders--acknowledge-order",
        operation_description="Acknowledge an order from a vendor and set the status to 'ACKNOWLEDGED'",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The po_number for the order to update",
            ),
        ],
        request_body=PurchaseOrderOnlyVendorSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The updated purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_404_NOT_FOUND: "Purchase order not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders Process Operations"],
    )
    def acknowledge(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # If the order is not issued
        if order.status in ["PENDING"]:
            return response.Response(
                {"status": "This order is not yet issued"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If the order is already acknowledged
        if order.status in ["ACKNOWLEDGED", "DELIVERED", "CANCELLED"]:
            return response.Response(
                {"status": "This order is already processed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deserialize and validate the data
        acknowledge_serializer = PurchaseOrderOnlyVendorSerializer(data=request.data)

        # If the provided data is valid
        if acknowledge_serializer.is_valid():
            # Check if the order issued vendor is the same as the acknowledged vendor
            if (
                order.vendor.vendor_code
                != acknowledge_serializer.validated_data["vendor"]
            ):
                return response.Response(
                    {"vendor": "This vendor is not the same as the issued vendor"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set the status to ACKNOWLEDGED
            order.status = "ACKNOWLEDGED"

            # Save the order
            order.save()

            # Serialize the updated purchase order
            serializer = PurchaseOrderSerializer(order)

            # Return the success response
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Return the error response
        return response.Response(
            acknowledge_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to update the purchase order and set the status to "DELIVERED"
    @swagger_auto_schema(
        operation_id="purchase_orders--deliver-order",
        operation_description="Deliver an order to a vendor and set the status to 'DELIVERED'",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The po_number for the order to update",
            ),
        ],
        request_body=PurchaseOrderOnlyVendorSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The updated purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_404_NOT_FOUND: "Purchase order not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders Process Operations"],
    )
    def deliver(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # If the order is not acknowledged
        if order.status in ["PENDING", "ISSUED"]:
            return response.Response(
                {"status": "This order is not yet acknowledged"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If the order is already delivered
        if order.status in ["DELIVERED", "CANCELLED"]:
            return response.Response(
                {"status": "This order is already processed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deserialize and validate the data
        deliver_serializer = PurchaseOrderOnlyVendorSerializer(data=request.data)

        # If the provided data is valid
        if deliver_serializer.is_valid():
            # Check if the order acknowledged vendor is the same as the delivered vendor
            if order.vendor.vendor_code != deliver_serializer.validated_data["vendor"]:
                return response.Response(
                    {
                        "vendor": "This vendor is not the same as the acknowledged vendor"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set the status to DELIVERED
            order.status = "DELIVERED"

            # Save the order
            order.save()

            # Serialize the updated purchase order
            serializer = PurchaseOrderSerializer(order)

            # Return the success response
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Return the error response
        return response.Response(
            deliver_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to update the purchase order and set the status to "CANCELLED"
    @swagger_auto_schema(
        operation_id="purchase_orders--cancel-order",
        operation_description="Cancel an order and set the status to 'CANCELLED'",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The po_number for the order to update",
            ),
        ],
        request_body=PurchaseOrderOnlyVendorSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The updated purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_404_NOT_FOUND: "Purchase order not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders Process Operations"],
    )
    def cancel(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # If the order is already delivered
        if order.status in ["DELIVERED", "CANCELLED"]:
            return response.Response(
                {"status": "This order is already processed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deserialize and validate the data
        cancel_serializer = PurchaseOrderOnlyVendorSerializer(data=request.data)

        # If the provided data is valid
        if cancel_serializer.is_valid():
            # Check if the order issued vendor is the same as the cancelled vendor
            if order.vendor.vendor_code != cancel_serializer.validated_data["vendor"]:
                return response.Response(
                    {"vendor": "This vendor is not the same as the issued vendor"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Set the status to CANCELLED
            order.status = "CANCELLED"

            # Save the order
            order.save()

            # Serialize the updated purchase order
            serializer = PurchaseOrderSerializer(order)

            # Return the success response
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Return the error response
        return response.Response(
            cancel_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to update the purchase order and set the quality rating
    @swagger_auto_schema(
        operation_id="purchase_orders--rate-quality",
        operation_description="Rate the quality of an order",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="string",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="po_number",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The po_number for the order to update",
            ),
        ],
        request_body=PurchaseOrderSetQualityRatingSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The updated purchase order", schema=PurchaseOrderSerializer
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_404_NOT_FOUND: "Purchase order not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Purchase Orders Process Operations"],
    )
    def rate_quality(self, request, po_number=None):
        # Get the order by po_number
        order = get_object_or_404(PurchaseOrder, po_number=po_number)

        # If the order is not delivered
        if order.status in ["PENDING", "ISSUED", "ACKNOWLEDGED"]:
            return response.Response(
                {"status": "This order is not yet delivered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If the order is already cancelled
        if order.status == "CANCELLED":
            return response.Response(
                {"status": "This order is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # If the order is already rated
        if order.quality_rating is not None:
            return response.Response(
                {"status": "This order is already rated"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Deserialize and validate the data
        rate_quality_serializer = PurchaseOrderSetQualityRatingSerializer(
            data=request.data
        )

        # If the provided data is valid
        if rate_quality_serializer.is_valid():
            # Set the quality rating
            order.quality_rating = rate_quality_serializer.validated_data[
                "quality_rating"
            ]

            # Save the order
            order.save()

            # Serialize the updated purchase order
            serializer = PurchaseOrderSerializer(order)

            # Return the success response
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Return the error response
        return response.Response(
            rate_quality_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
