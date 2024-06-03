# Imports
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


# App configuration
class HistoricalPerformancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor_management_system.historical_performances"
    verbose_name = _("Historical Performances")
