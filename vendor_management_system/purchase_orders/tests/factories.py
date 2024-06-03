# Imports
import datetime
import uuid

import factory
from faker import Faker
from vendor_management_system.purchase_orders.models import PurchaseOrder

from vendor_management_system.vendors.tests.factories import VendorFactory


# Initialize the Faker library
faker = Faker()


# Factory to create a PurchaseOrder object
class PurchaseOrderFactory(factory.django.DjangoModelFactory):
    # Set the PurchaseOrder model
    class Meta:
        model = PurchaseOrder

    # Set the fields for the PurchaseOrder model
    po_number = factory.LazyFunction(
        lambda: str(uuid.uuid4()).replace("-", "")[:10].upper()
    )
    order_date = factory.LazyFunction(faker.date_time_this_year)
    items = factory.LazyFunction(
        lambda: [
            {"item": faker.word(), "quantity": faker.random_int(min=1, max=10)}
            for _ in range(faker.random_int(min=1, max=5))
        ]
    )
    quantity = factory.LazyFunction(lambda: faker.random_int(min=1, max=100))
    status = factory.LazyFunction(
        lambda: faker.random_element(
            elements=["PENDING", "ISSUED", "ACKNOWLEDGED", "DELIVERED", "CANCELLED"]
        )
    )
    quality_rating = factory.LazyFunction(
        lambda: faker.random_element(elements=[1, 2, 3, 4, 5])
    )

    # Ensuring that the vendor is consistent
    @factory.lazy_attribute
    def vendor(self):
        if self.status == "PENDING":
            return None
        return VendorFactory()

    # Ensuring that the issue_date is consistent
    @factory.lazy_attribute
    def issue_date(self):
        if self.status in ["ISSUED", "ACKNOWLEDGED", "DELIVERED", "CANCELLED"]:
            return faker.date_time_between_dates(
                datetime_start=self.order_date,
                datetime_end=self.order_date + datetime.timedelta(days=7),
            )
        return None

    # Ensuring that the acknowledgment_date is consistent
    @factory.lazy_attribute
    def acknowledgment_date(self):
        if self.status in ["ACKNOWLEDGED", "DELIVERED", "CANCELLED"]:
            return faker.date_time_between_dates(
                datetime_start=self.issue_date,
                datetime_end=self.issue_date + datetime.timedelta(days=7),
            )
        return None

    # Ensuring that the expected_delivery_date is consistent
    @factory.lazy_attribute
    def expected_delivery_date(self):
        if self.status in ["PENDING", "CANCELLED"]:
            return self.order_date + datetime.timedelta(days=21)
        elif self.status == "ISSUED":
            return self.issue_date + datetime.timedelta(days=14)
        elif self.status == ["ACKNOWLEDGED", "DELIVERED"]:
            return self.acknowledgment_date + datetime.timedelta(days=7)
        return None

    # Ensuring that the actual_delivery_date is consistent
    @factory.lazy_attribute
    def actual_delivery_date(self):
        if self.status == "DELIVERED":
            return faker.date_time_between_dates(
                datetime_start=self.acknowledgment_date,
                datetime_end=self.acknowledgment_date + datetime.timedelta(days=7),
            )
        return None
