# Django starts so that shared_task will use this app.
from .celery_app import app as celery_app


# Define which symbols will be imported when using "from <module> import *"
__all__ = ("celery_app",)
