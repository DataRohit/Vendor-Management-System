# Imports
from django.urls import path

from vendor_management_system.users.views import UserViewSet


# Define the URL patterns for the users app
urlpatterns = [
    path(
        "",
        UserViewSet.as_view({"get": "list"}),
        name="users--list-users",
    ),
    path(
        "<email>/",
        UserViewSet.as_view({"get": "retrieve"}),
        name="users--retrieve-user",
    ),
]
