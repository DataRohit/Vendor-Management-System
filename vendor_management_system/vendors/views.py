# Imports
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, response, status, viewsets

from vendor_management_system.core.authentication import (
    QueryParameterTokenAuthentication,
)

from vendor_management_system.vendors.models import Vendor
from vendor_management_system.vendors.serializers import (
    VendorCreateUpdateSerializer,
    VendorSerializer,
)


# Class based ViewSet for Vendor
class VendorViewSet(viewsets.ViewSet):
    # Set the permission and authentication classes
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [QueryParameterTokenAuthentication]

    # Method to handle listing all vendors
    @swagger_auto_schema(
        operation_id="vendors--list-vendors",
        operation_description="List all vendors",
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
                "List of all vendors", schema=VendorSerializer(many=True)
            ),
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Vendors"],
    )
    def list(self, request):
        # Get all vendors
        vendors = Vendor.objects.all()

        # Serialize the vendors
        serializer = VendorSerializer(vendors, many=True)

        # Return the response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    # Method to handle new vendor creation
    @swagger_auto_schema(
        operation_id="vendors--create-vendor",
        operation_description="Create a new vendor",
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
        request_body=VendorCreateUpdateSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Response(
                "The created vendor", schema=VendorSerializer
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Vendors"],
    )
    def create(self, request):
        # Deserialize and validate the request data
        vendor_create_serializer = VendorCreateUpdateSerializer(data=request.data)

        # If the provided data is valid
        if vendor_create_serializer.is_valid():
            # Deserialize and validate the data
            vendor_serializer = VendorSerializer(
                data=vendor_create_serializer.validated_data
            )

            # If the vendor is valid
            if vendor_serializer.is_valid():
                # Create a new Vendor object
                vendor = Vendor.objects.create(**vendor_serializer.validated_data)

                # Serialize the vendor
                vendor_serializer = VendorSerializer(vendor)

                # Return the response
                return response.Response(
                    vendor_serializer.data, status=status.HTTP_201_CREATED
                )

            else:
                # Return the response
                return response.Response(
                    vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        # Return the error response
        return response.Response(
            vendor_create_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to handle retrieving a single vendor
    @swagger_auto_schema(
        operation_id="vendors--retrieve-vendor",
        operation_description="Retrieve a specific vendor's details",
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
                name="vendor_code",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The vendor_code for the vendor to retrieve",
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The retrieved vendor", schema=VendorSerializer
            ),
            status.HTTP_404_NOT_FOUND: "Vendor not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Vendors"],
    )
    def retrieve(self, request, vendor_code=None):
        # Get the vendor by vendor_code
        vendor = get_object_or_404(Vendor, vendor_code=vendor_code)

        # Serialize the vendor
        serializer = VendorSerializer(vendor)

        # Return the response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    # Method to handle updating a vendor
    @swagger_auto_schema(
        operation_id="vendors--update-vendor",
        operation_description="Update a specific vendor",
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
                name="vendor_code",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The vendor_code for the vendor to update",
            ),
        ],
        request_body=VendorCreateUpdateSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                "The updated vendor", schema=VendorSerializer
            ),
            status.HTTP_400_BAD_REQUEST: "Bad request",
            status.HTTP_404_NOT_FOUND: "Vendor not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Vendors"],
    )
    def update(self, request, vendor_code=None):
        # Get the vendor by vendor_code
        vendor = get_object_or_404(Vendor, vendor_code=vendor_code)

        # Deserialize and validate the data
        vendor_update_serializer = VendorCreateUpdateSerializer(
            vendor, data=request.data, partial=True
        )

        # If the provided data is valid
        if vendor_update_serializer.is_valid():
            # Save the vendor
            vendor_update_serializer.save()

            # Fetch the updated vendor
            vendor = Vendor.objects.get(vendor_code=vendor_code)

            # Serialize the vendor
            serializer = VendorSerializer(vendor)

            # Return the response
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        # Return the error response
        return response.Response(
            vendor_update_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    # Method to handle deleting a vendor
    @swagger_auto_schema(
        operation_id="vendors--destroy-vendor",
        operation_description="Delete a specific vendor",
        manual_parameters=[
            openapi.Parameter(
                name="token",
                format="<string>",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
                description="The token to authenticate the user",
            ),
            openapi.Parameter(
                name="vendor_code",
                format="<string>",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The vendor_code for the vendor to delete",
            ),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: "Vendor deleted",
            status.HTTP_404_NOT_FOUND: "Vendor not found",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Vendors"],
    )
    def destroy(self, request, vendor_code=None):
        # Get the vendor by vendor_code
        vendor = get_object_or_404(Vendor, vendor_code=vendor_code)

        # Delete the vendor
        vendor.delete()

        # Return the response
        return response.Response(status=status.HTTP_204_NO_CONTENT)
