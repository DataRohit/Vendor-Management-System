# Imports
import pytest

from vendor_management_system.historical_performances.tests.factories import (
    HistoricalPerformanceFactory,
)

from vendor_management_system.purchase_orders.tests.factories import (
    PurchaseOrderFactory,
)

from vendor_management_system.vendors.tests.factories import VendorFactory


# Set the fixture for the VendorFactory
@pytest.fixture()
def vendor_factory(db) -> VendorFactory:
    return VendorFactory


# Set the fixture for the PurchaseOrderFactory
@pytest.fixture()
def purchase_order_factory(db) -> PurchaseOrderFactory:
    return PurchaseOrderFactory


# Set the fixture for the HistoricalPerformanceFactory
@pytest.fixture()
def historical_performance_factory(db) -> HistoricalPerformanceFactory:
    return HistoricalPerformanceFactory
