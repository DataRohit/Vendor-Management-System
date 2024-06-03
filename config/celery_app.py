# Imports
import os

from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


# Instantiate the Celery application with a name.
app = Celery("vendor_management_system")


# Load the Django settings module for Celery configuration using a namespace.
# The 'namespace' argument defines the prefix for Celery-related settings in Django settings.
app.config_from_object("django.conf:settings", namespace="CELERY")


# Automatically discover tasks from all installed apps in the Django project.
app.autodiscover_tasks()
