# Imports
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, response, status, viewsets

from vendor_management_system.core.authentication import (
    QueryParameterTokenAuthentication,
)

from vendor_management_system.users.models import User
from vendor_management_system.users.serializers import UserSerializer


# Class based ViewSet for User
class UserViewSet(viewsets.ViewSet):
    # Set the permission and authentication classes
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [QueryParameterTokenAuthentication]

    # Method to handle listing all users
    @swagger_auto_schema(
        operation_id="users--list-users",
        operation_description="List all users",
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
                "List of all users", schema=UserSerializer(many=True)
            ),
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
        },
        tags=["Users"],
    )
    def list(self, request):
        # Get all users
        users = User.objects.all()

        # Serialize the users
        serializer = UserSerializer(users, many=True)

        # Return the response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    # Method to handle retrieving a single user
    @swagger_auto_schema(
        operation_id="users--retrieve-user",
        operation_description="Retrieve a single user",
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
                name="email",
                format="string",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                required=True,
                description="The email of the user to retrieve",
            ),
        ],
        responses={
            status.HTTP_200_OK: openapi.Response("The user", schema=UserSerializer()),
            status.HTTP_401_UNAUTHORIZED: "Unauthorized",
            status.HTTP_404_NOT_FOUND: "User not found",
        },
        tags=["Users"],
    )
    def retrieve(self, request, email=None):
        # Get the user by email
        user = get_object_or_404(User, email=email)

        # Serialize the user
        serializer = UserSerializer(user)

        # Return the response
        return response.Response(serializer.data, status=status.HTTP_200_OK)
