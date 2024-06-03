# Imports
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer


# Query Param Auth Token Serializer
class QueryParamAuthTokenSerializer(AuthTokenSerializer):
    # Fields
    username = None
    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label="Token", read_only=True)

    # Method to validate
    def validate(self, attrs):
        # Get the email and password
        email = attrs.get("email")
        password = attrs.get("password")

        # If both username and password are set
        if email and password:
            # Authenticate the user
            user = authenticate(
                request=self.context.get("request"), username=email, password=password
            )

            # If the user is not found
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        # Set the user
        attrs["user"] = user

        # Return the attributes
        return attrs
