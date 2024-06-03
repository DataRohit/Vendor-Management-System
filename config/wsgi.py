# Imports
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application


# Resolve the base directory of the project
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Add the project directory to the Python path
sys.path.append(str(BASE_DIR / "vendor_management_system"))


# Set the Django settings module to use for the application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


# Get the WSGI application for the Django project
application = get_wsgi_application()
