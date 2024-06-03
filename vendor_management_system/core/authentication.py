# Imports
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


# Custom token authentication
class QueryParameterTokenAuthentication(TokenAuthentication):
    # Method to authenticate
    def authenticate(self, request):
        # Get the token from the query parameters
        token = request.GET.get("token")

        # Check if the token is set
        if token:
            # Try to authenticate the credentials
            try:
                return self.authenticate_credentials(token)

            # If the authentication fails return None
            except AuthenticationFailed:
                return None

        # If the token is not set return None
        return None
