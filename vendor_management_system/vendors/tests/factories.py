# Imports
import uuid

import factory
from faker import Faker

from vendor_management_system.vendors.models import Vendor


# Initialize the Faker library
faker = Faker()


# Factory to create a Vendor object
class VendorFactory(factory.django.DjangoModelFactory):
    # Set the Vendor model
    class Meta:
        model = Vendor

    # Set the fields for the Vendor model
    vendor_code = factory.LazyFunction(
        lambda: str(uuid.uuid4()).replace("-", "")[:10].upper()
    )
    name = factory.LazyFunction(faker.company)
    contact_details = factory.LazyFunction(
        lambda: f"{faker.email()}, {faker.phone_number()}"
    )
    address = factory.LazyFunction(faker.address)
    on_time_delivery_rate = factory.LazyFunction(
        lambda: faker.pyfloat(min_value=0, max_value=100, right_digits=4)
    )
    quality_rating_avg = factory.LazyFunction(
        lambda: faker.pyfloat(min_value=0, max_value=5, right_digits=4)
    )
    average_response_time = factory.LazyFunction(
        lambda: faker.pyfloat(min_value=0, right_digits=4)
    )
    fulfillment_rate = factory.LazyFunction(
        lambda: faker.pyfloat(min_value=0, max_value=100, right_digits=4)
    )
