# Imports
import pytest

from vendor_management_system.users.models import User


# Class to test the UserManager
@pytest.mark.django_db()
class TestUserManager:
    # Method to test the create_user method
    def test_create_user(self):
        # Create a new user
        user = User.object.create_user(
            name="Test User",
            email="testuser@example.com",
            password="Test-R@nd0m-P@ssw0rd",
        )

        # Assert that the user is created successfully
        assert user.name == "Test User"
        assert user.email == "testuser@example.com"
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password("Test-R@nd0m-P@ssw0rd") is True

    # Method to test the create_user method with is_staff or is_superuser set to True
    def test_create_user_with_is_staff_or_is_superuser_set_to_true(self):
        # Create a new user with is_staff and is_superuser set to True
        with pytest.raises(ValueError):
            User.object.create_user(
                name="Test User",
                email="testuser@example.com",
                password="Test-R@nd0m-P@ssw0rd",
                is_staff=True,
                is_superuser=True,
            )

    # Method to test the create_superuser method
    def test_create_superuser(self):
        # Create a new superuser
        user = User.object.create_superuser(
            name="Test Admin",
            email="testadmin@example.com",
            password="Admin-R@nd0m-P@ssw0rd",
        )

        # Assert that the user is created successfully
        assert user.name == "Test Admin"
        assert user.email == "testadmin@example.com"
        assert user.is_staff is True
        assert user.is_superuser is True
        assert user.check_password("Admin-R@nd0m-P@ssw0rd") is True

    # Method to test the create_superuser method with is_staff or is_superuser set to False
    def test__create_superuser_with_is_staff_or_is_superuser_set_to_false(self):
        # Create a new admin user with is_staff and is_superuser set to False
        with pytest.raises(ValueError):
            User.object.create_superuser(
                name="Admin User",
                email="adminuser@example.com",
                password="Admin-R@nd0m-P@ssw0rd",
                is_staff=False,
                is_superuser=False,
            )
