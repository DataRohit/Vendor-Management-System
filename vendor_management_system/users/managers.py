# Imports
from django.contrib.auth.models import UserManager as DjangoUserManager


# Manager for User model
class UserManager(DjangoUserManager):
    # Method to create a user
    def _create_user(self, email: str, password: str | None, **extra_fields):
        # Check if email is provided
        if not email:
            raise ValueError("The Email field must be set")

        # Normalize email
        email = self.normalize_email(email)

        # Create user instance
        user = self.model(email=email, **extra_fields)

        # Set password
        user.set_password(password)

        # Save user
        user.save(using=self._db)

        # Return user
        return user

    # Method to create a normal user
    def create_user(self, email: str, password: str | None = None, **extra_fields):
        # Set default values for is_staff and is_superuser
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        # Ensure is_staff and is_superuser are not True for normal users
        if extra_fields.get("is_staff") or extra_fields.get("is_superuser"):
            raise ValueError(
                "Normal user cannot have is_staff or is_superuser set to True."
            )

        # Create user
        return self._create_user(email, password, **extra_fields)

    # Method to create a superuser
    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        # Set default values for is_staff and is_superuser
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Ensure is_staff and is_superuser are set to True for superusers
        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError(
                "Superuser must have is_staff and is_superuser set to True."
            )

        # Create superuser
        return self._create_user(email, password, **extra_fields)
