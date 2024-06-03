# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# App configuration
class PurchaseOrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_management_system.purchase_orders"
    verbose_name = _("Purchase Orders")

    # Ready method
    def ready(self):
        # Import the signals module
        import vendor_management_system.purchase_orders.signals
