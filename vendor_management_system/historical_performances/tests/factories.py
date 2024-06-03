# Imports
import uuid

import factory
from faker import Faker

from vendor_management_system.historical_performances.models import (
    HistoricalPerformance,
)
from vendor_management_system.vendors.tests.factories import VendorFactory


# Initialize the Faker library
faker = Faker()


# Factory to create a HistoricalPerformance object
class HistoricalPerformanceFactory(factory.django.DjangoModelFactory):
    # Set the HistoricalPerformance model
    class Meta:
        model = HistoricalPerformance

    # Set the fields for the HistoricalPerformance model
    id = factory.LazyFunction(lambda: str(uuid.uuid4()).replace("-", "")[:10].upper())
    vendor = factory.SubFactory(VendorFactory)
    date = factory.LazyFunction(faker.date_time_this_year)
    on_time_delivery_rate = factory.LazyFunction(
        lambda: faker.random_int(min=0, max=100)
    )
    quality_rating_avg = factory.LazyFunction(lambda: faker.random_int(min=0, max=5))
    average_response_time = factory.LazyFunction(
        lambda: faker.random_int(min=0, max=100)
    )
    fulfillment_rate = factory.LazyFunction(lambda: faker.random_int(min=0, max=100))
