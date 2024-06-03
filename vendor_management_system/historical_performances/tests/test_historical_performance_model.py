# Imports
from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from vendor_management_system.vendors.models import Vendor


# Test the HistoricalPerformance object creation
@pytest.mark.django_db
def test_historical_performance_model_fields(
    db, historical_performance_factory, vendor_factory
):
    # Create a Vendor object
    vendor = vendor_factory()

    # Test for 5 HistoricalPerformance objects
    for _ in range(5):
        historical_performance = historical_performance_factory(vendor=vendor)

        # Check the HistoricalPerformance object fields
        assert historical_performance.id is not None
        assert historical_performance.vendor is not None
        assert historical_performance.date is not None
        assert historical_performance.on_time_delivery_rate is not None
        assert historical_performance.quality_rating_avg is not None
        assert historical_performance.average_response_time is not None
        assert historical_performance.fulfillment_rate is not None

        # Check the HistoricalPerformance object field types
        assert isinstance(historical_performance.id, str)
        assert isinstance(historical_performance.vendor, Vendor)
        assert isinstance(historical_performance.date, datetime)
        assert isinstance(historical_performance.on_time_delivery_rate, int)
        assert isinstance(historical_performance.quality_rating_avg, int)
        assert isinstance(historical_performance.average_response_time, int)
        assert isinstance(historical_performance.fulfillment_rate, int)

        # Check the HistoricalPerformance object field values
        assert (
            historical_performance.on_time_delivery_rate >= 0
            and historical_performance.on_time_delivery_rate <= 100
        )
        assert (
            historical_performance.quality_rating_avg >= 0
            and historical_performance.quality_rating_avg <= 5
        )
        assert (
            historical_performance.average_response_time >= 0
            and historical_performance.average_response_time <= 100
        )
        assert (
            historical_performance.fulfillment_rate >= 0
            and historical_performance.fulfillment_rate <= 100
        )


# Test for valid Historical Performance ID format
@pytest.mark.django_db
def test_historical_performance_id_format(db, historical_performance_factory):
    # Lists specifying valid and invalid historical performance IDs
    invalid_ids = [
        "hpr001",
        "Hpr001",
        "HPR 003",
        "HPR-004",
        "HPR@005",
    ]

    # Check all invalid historical performance IDs raise a ValidationError
    for invalid_id in invalid_ids:
        with pytest.raises(ValidationError):
            historical_performance = historical_performance_factory(id=invalid_id)
            historical_performance.full_clean()


# Test for unique Historical Performance ID
@pytest.mark.django_db
def test_unique_historical_performance_id(db, historical_performance_factory):
    # Create a HistoricalPerformance object with a historical performance ID
    historical_performance = historical_performance_factory()

    # Check that creating another HistoricalPerformance object with the same Historical Performance ID raises an IntegrityError
    with pytest.raises(IntegrityError):
        historical_performance_duplicate = historical_performance_factory(
            id=historical_performance.id
        )
        historical_performance_duplicate.full_clean()
