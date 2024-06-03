# Imports
from datetime import datetime

import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from vendor_management_system.vendors.models import Vendor


# Test the PurchaseOrder object creation
@pytest.mark.django_db
def test_purchase_order_model_fields(db, purchase_order_factory):
    # Test for 5 PurchaseOrder objects
    for status in ["PENDING", "ISSUED", "ACKNOWLEDGED", "DELIVERED", "CANCELLED"]:
        purchase_order = purchase_order_factory(status=status)

        # Check the PurchaseOrder object fields
        assert purchase_order.po_number is not None
        assert purchase_order.order_date is not None
        assert purchase_order.items is not None
        assert purchase_order.quantity is not None
        assert purchase_order.status is not None
        assert purchase_order.quality_rating is not None

        # Check the PurchaseOrder object field types
        assert isinstance(purchase_order.po_number, str)
        assert isinstance(purchase_order.vendor, (Vendor, type(None)))
        assert isinstance(purchase_order.order_date, datetime)
        assert isinstance(purchase_order.items, list)
        assert isinstance(purchase_order.quantity, int)
        assert isinstance(purchase_order.status, str)
        assert isinstance(purchase_order.quality_rating, int)

        # Check the PurchaseOrder object field values
        assert purchase_order.quantity >= 1 and purchase_order.quantity <= 100
        assert purchase_order.status == status
        assert purchase_order.quality_rating in [1, 2, 3, 4, 5]


# Test for valid Purchase Order Number format
@pytest.mark.django_db
def test_po_number_format(db, purchase_order_factory):
    # Lists specifying valid and invalid purchase order numbers
    invalid_po_numbers = [
        "po001",
        "Po002",
        "PO 003",
        "PO-004",
        "PO@005",
    ]

    # Check all invalid purchase order numbers raise a ValidationError
    for invalid_number in invalid_po_numbers:
        with pytest.raises(ValidationError):
            purchase_order = purchase_order_factory(po_number=invalid_number)
            purchase_order.full_clean()


# Test for unique Purchase Order Number
@pytest.mark.django_db
def test_unique_po_number(db, purchase_order_factory):
    # Create a PurchaseOrder object with a purchase order number
    purchase_order = purchase_order_factory()

    # Check that creating another PurchaseOrder object with the same Purchase Order Number raises an IntegrityError
    with pytest.raises(IntegrityError):
        purchase_order_duplicate = purchase_order_factory(
            po_number=purchase_order.po_number
        )
        purchase_order_duplicate.full_clean()


# Test for valid dates - status "PENDING"
@pytest.mark.django_db
def test_valid_dates_status_pending(db, purchase_order_factory):
    # Create a PurchaseOrder object with a status of "PENDING"
    purchase_order = purchase_order_factory(status="PENDING")

    # If the status is "PENDING", the issue_date, acknowledgment_date and actual_delivery_date should be None
    assert purchase_order.issue_date is None
    assert purchase_order.acknowledgment_date is None
    assert purchase_order.actual_delivery_date is None

    # If the status is "PENDING", the expected_delivery_date should be after the order_date
    assert purchase_order.expected_delivery_date >= purchase_order.order_date


# Test for valid dates - status "ISSUED"
def test_valid_dates_status_issued(db, purchase_order_factory):
    # Create a PurchaseOrder object with a status of "ISSUED"
    purchase_order = purchase_order_factory(status="ISSUED")

    # If the status is "ISSUED", the issue_date should be after the order_date
    assert purchase_order.issue_date >= purchase_order.order_date

    # If the status is "ISSUED", the acknowledgment_date and actual_delivery_date should be None
    assert purchase_order.acknowledgment_date is None
    assert purchase_order.actual_delivery_date is None

    # If the status is "ISSUED", the expected_delivery_date should be after the issue_date
    assert purchase_order.expected_delivery_date >= purchase_order.issue_date


# Test for valid dates - status "ACKNOWLEDGED"
def test_valid_dates_status_acknowledged(db, purchase_order_factory):
    # Create a PurchaseOrder object with a status of "ACKNOWLEDGED"
    purchase_order = purchase_order_factory(status="ACKNOWLEDGED")

    # If the status is "ACKNOWLEDGED", the issue_date should be after the order_date
    assert purchase_order.issue_date >= purchase_order.order_date

    # If the status is "ACKNOWLEDGED", the acknowledgment_date should be after the issue_date
    assert purchase_order.acknowledgment_date >= purchase_order.issue_date

    # IF the status is "ACKNOWLEDGED", the actual_delivery_date should be None
    assert purchase_order.actual_delivery_date is None

    # If the status is "ACKNOWLEDGED", the expected_delivery_date should be after the acknowledgment_date
    assert purchase_order.expected_delivery_date >= purchase_order.acknowledgment_date


# Test for valid dates - status "DELIVERED"
def test_valid_dates_status_delivered(db, purchase_order_factory):
    # Create a PurchaseOrder object with a status of "DELIVERED"
    purchase_order = purchase_order_factory(status="DELIVERED")

    # If the status is "DELIVERED", the issue_date should be after the order_date
    assert purchase_order.issue_date >= purchase_order.order_date

    # If the status is "DELIVERED", the acknowledgment_date should be after the issue_date
    assert purchase_order.acknowledgment_date >= purchase_order.issue_date

    # If the status is "DELIVERED", the expected_delivery_date and actual_delivery_date should be after the acknowledgment_date
    assert purchase_order.expected_delivery_date >= purchase_order.acknowledgment_date
    assert purchase_order.actual_delivery_date >= purchase_order.acknowledgment_date


# Test for valid dates - status "CANCELLED"
def test_valid_dates_status_cancelled(db, purchase_order_factory):
    # Create a PurchaseOrder object with a status of "CANCELLED"
    purchase_order = purchase_order_factory(status="CANCELLED")

    # If the status is "CANCELLED", the issue_date should be after the order_date
    assert purchase_order.issue_date >= purchase_order.order_date

    # If the status is "CANCELLED", the acknowledgment_date should be after the issue_date
    assert purchase_order.acknowledgment_date >= purchase_order.issue_date

    # If the status is "CANCELLED", the expected_delivery_date should be after the acknowledgment_date
    assert purchase_order.expected_delivery_date >= purchase_order.acknowledgment_date

    # If the status is "CANCELLED", the actual_delivery_date should be None
    assert purchase_order.actual_delivery_date is None
