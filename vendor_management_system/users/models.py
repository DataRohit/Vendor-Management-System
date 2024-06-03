# Imports
import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField
from django.utils.translation import gettext_lazy as _

from vendor_management_system.users.managers import UserManager


# Model for User
class User(AbstractUser):
    # Fields
    id = CharField(_("ID of User"), primary_key=True, editable=False, default=uuid.uuid4)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None
    last_name = None
    email = EmailField(_("Email Address"), unique=True)
    username = None

    # Username Field
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    # Required Fields
    REQUIRED_FIELDS = ["name"]

    # Manager
    object: ClassVar[UserManager] = UserManager()
