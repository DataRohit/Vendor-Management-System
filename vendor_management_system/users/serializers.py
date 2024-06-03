# Imports
from rest_framework.serializers import ModelSerializer

from vendor_management_system.users.models import User


# Serializer for User
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
        ]
