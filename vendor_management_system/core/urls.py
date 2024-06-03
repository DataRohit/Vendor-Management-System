# Imports
from django.urls import path

from vendor_management_system.core.views import QueryParamObtainAuthToken


# Add the URL patterns for the core app
urlpatterns = [
    path(
        "obtain-auth-token/",
        QueryParamObtainAuthToken.as_view(),
        name="core--obtain-auth-token",
    ),
]
