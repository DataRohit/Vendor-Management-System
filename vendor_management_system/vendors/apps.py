# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# App configuration
class VendorsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_management_system.vendors"
    verbose_name = _("Vendors")
