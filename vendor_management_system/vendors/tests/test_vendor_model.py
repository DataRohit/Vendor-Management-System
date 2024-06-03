# Imports
import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError


# Test the Vendor object creation
@pytest.mark.django_db
def test_vendor_model_fields(db, vendor_factory):
    # Test for 5 Vendor objects
    for _ in range(5):
        vendor = vendor_factory()

        # Check the Vendor object fields
        assert vendor.vendor_code is not None
        assert vendor.name is not None
        assert vendor.contact_details is not None
        assert vendor.address is not None
        assert vendor.on_time_delivery_rate is not None
        assert vendor.quality_rating_avg is not None
        assert vendor.average_response_time is not None
        assert vendor.fulfillment_rate is not None

        # Check the Vendor object field types
        assert isinstance(vendor.vendor_code, str)
        assert isinstance(vendor.name, str)
        assert isinstance(vendor.contact_details, str)
        assert isinstance(vendor.address, str)
        assert isinstance(vendor.on_time_delivery_rate, float)
        assert isinstance(vendor.quality_rating_avg, float)
        assert isinstance(vendor.average_response_time, float)
        assert isinstance(vendor.fulfillment_rate, float)

        # Check the Vendor object field values
        assert vendor.on_time_delivery_rate >= 0 and vendor.on_time_delivery_rate <= 100
        assert vendor.quality_rating_avg >= 0 and vendor.quality_rating_avg <= 5
        assert vendor.average_response_time >= 0
        assert vendor.fulfillment_rate >= 0 and vendor.fulfillment_rate <= 100


# Test for valid Vendor Code format
@pytest.mark.django_db
def test_vendor_code_format(db, vendor_factory):
    # Lists specifying valid and invalid vendor codes
    invalid_vendor_codes = [
        "vnd001",
        "Vnd002",
        "VND 003",
        "VND-004",
        "VND@005",
    ]

    # Check all invalid vendor codes raise a ValidationError
    for invalid_code in invalid_vendor_codes:
        with pytest.raises(ValidationError):
            vendor = vendor_factory(vendor_code=invalid_code)
            vendor.full_clean()


# Test for unique Vendor Code
@pytest.mark.django_db
def test_vendor_code_unique(db, vendor_factory):
    # Create a Vendor object with a vendor code
    vendor = vendor_factory()

    # Create a new Vendor object with the same vendor code
    with pytest.raises(IntegrityError):
        vendor_duplicate = vendor_factory(vendor_code=vendor.vendor_code)
        vendor_duplicate.full_clean()


# Test for Vendor on-time delivery rate
@pytest.mark.django_db
def test_vendor_on_time_delivery_rate(db, vendor_factory):
    # Lists specifying valid and invalid on-time delivery rates
    invalid_on_time_delivery_rates = [
        -1,
        101,
    ]

    # Check all invalid on-time delivery rates raise a ValidationError
    for invalid_rate in invalid_on_time_delivery_rates:
        with pytest.raises(ValidationError):
            vendor = vendor_factory(on_time_delivery_rate=invalid_rate)
            vendor.full_clean()


# Test for Vendor quality rating average
@pytest.mark.django_db
def test_vendor_quality_rating_avg(db, vendor_factory):
    # Lists specifying valid and invalid quality rating averages
    invalid_quality_rating_avgs = [
        -1,
        6,
    ]

    # Check all invalid quality rating averages raise a ValidationError
    for invalid_avg in invalid_quality_rating_avgs:
        with pytest.raises(ValidationError):
            vendor = vendor_factory(quality_rating_avg=invalid_avg)
            vendor.full_clean()


# Test for Vendor average response time
@pytest.mark.django_db
def test_vendor_average_response_time(db, vendor_factory):
    # Lists specifying valid and invalid average response times
    invalid_average_response_times = [
        -1,
    ]

    # Check all invalid average response times raise a ValidationError
    for invalid_time in invalid_average_response_times:
        with pytest.raises(ValidationError):
            vendor = vendor_factory(average_response_time=invalid_time)
            vendor.full_clean()


# Test for Vendor fulfillment rate
@pytest.mark.django_db
def test_vendor_fulfillment_rate(db, vendor_factory):
    # Lists specifying valid and invalid fulfillment rates
    invalid_fulfillment_rates = [
        -1,
        101,
    ]

    # Check all invalid fulfillment rates raise a ValidationError
    for invalid_rate in invalid_fulfillment_rates:
        with pytest.raises(ValidationError):
            vendor = vendor_factory(fulfillment_rate=invalid_rate)
            vendor.full_clean()
