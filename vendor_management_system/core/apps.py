# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# App configuration
class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_management_system.core"
    verbose_name = _("Core")
