# Imports
import time
import warnings

from celery import shared_task
from django.db import transaction
from django.utils import timezone

from vendor_management_system.historical_performances.models import (
    HistoricalPerformance,
)

from vendor_management_system.vendors.models import Vendor


# Task to add a new record for the historical performance
@shared_task
def record_historical_performance(*args):
    # Ignore all the warnings
    warnings.filterwarnings("ignore")

    # Run the code and rollback the transaction if an exception occurs
    with transaction.atomic():
        # Get all the vendors
        vendors = Vendor.objects.all()

        # Loop through all the vendors
        for vendor in vendors:
            # Create a new historical performance record
            historical_performance = HistoricalPerformance(
                vendor=vendor,
                date=timezone.now(),
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate,
            )

            # Save the historical performance record
            historical_performance.save()
