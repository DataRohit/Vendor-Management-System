# Imports
import random
import warnings

from celery import chain, shared_task
from django.db import transaction
from django.utils.timezone import datetime, timedelta
from faker import Faker

from vendor_management_system.purchase_orders.models import PurchaseOrder
from vendor_management_system.vendors.models import Vendor


# Initialize the Faker
fake = Faker()


# Task to issue a purchase order
@shared_task
def issue_orders(*args):
    # Ignore all the warnings
    warnings.filterwarnings("ignore")

    # Run the code and rollback the transaction if an exception occurs
    with transaction.atomic():
        # Get all the vendors and pending orders
        vendors = Vendor.objects.all()
        pending_orders = PurchaseOrder.objects.filter(status="PENDING")

        # Randomly sample the vendors and orders
        sample_size = min(100, pending_orders.count())
        selected_vendors = random.sample(list(vendors), sample_size)
        selected_orders = random.sample(list(pending_orders), sample_size)

        # Issue the orders to the vendors
        for order, vendor in zip(selected_orders, selected_vendors):
            # Update order details
            order.vendor = vendor
            order.status = "ISSUED"
            order.issue_date = fake.date_time_between_dates(
                datetime_start=order.order_date + timedelta(days=1),
                datetime_end=order.order_date + timedelta(days=3),
            )

            # Save the order
            order.save()


# Task to acknowledge a purchase order
@shared_task
def acknowledge_orders(*args):
    # Ignore all the warnings
    warnings.filterwarnings("ignore")

    # Run the code and rollback the transaction if an exception occurs
    with transaction.atomic():
        # Get all the issued orders
        issued_orders = PurchaseOrder.objects.filter(status="ISSUED")

        # Randomly sample the orders
        sample_size = min(80, issued_orders.count())
        selected_orders = random.sample(list(issued_orders), sample_size)

        # Acknowledge the orders
        for order in selected_orders:
            # Update order details
            order.status = "ACKNOWLEDGED"
            order.acknowledgment_date = fake.date_time_between_dates(
                datetime_start=order.issue_date + timedelta(hours=6),
                datetime_end=order.issue_date + timedelta(days=3),
            )

            # Save the order
            order.save()


# Task to deliver a purchase order
@shared_task
def deliver_orders(*args):
    # Ignore all the warnings
    warnings.filterwarnings("ignore")

    # Run the code and rollback the transaction if an exception occurs
    with transaction.atomic():
        # Get all the acknowledged orders
        acknowledged_orders = PurchaseOrder.objects.filter(status="ACKNOWLEDGED")

        # Randomly sample the orders
        sample_size = min(40, acknowledged_orders.count())
        selected_orders = random.sample(list(acknowledged_orders), sample_size)

        # Deliver the orders
        for order in selected_orders:
            # Update order details
            order.status = "DELIVERED"
            order.actual_delivery_date = fake.date_time_between_dates(
                datetime_start=order.expected_delivery_date - timedelta(days=2),
                datetime_end=order.expected_delivery_date + timedelta(days=2),
            )

            # Save the order
            order.save()


# Task to cancel the purchase order
@shared_task
def cancel_orders(*args):
    # Ignore all the warnings
    warnings.filterwarnings("ignore")

    # Run the code and rollback the transaction if an exception occurs
    with transaction.atomic():
        # Get all the pending, issued and acknowledged orders
        pending_orders = PurchaseOrder.objects.filter(
            status__in=["PENDING", "ISSUED", "ACKNOWLEDGED"]
        )

        # Randomly sample the orders
        sample_size = min(5, pending_orders.count())
        selected_orders = random.sample(list(pending_orders), sample_size)

        # Cancel the orders
        for order in selected_orders:
            # Update order details
            order.status = "CANCELLED"

            # Save the order
            order.save()


# Task to rate the purchase order
@shared_task
def rate_orders(*args):
    # Ignore all the warnings
    warnings.filterwarnings("ignore")

    # Run the code and rollback the transaction if an exception occurs
    with transaction.atomic():
        # Get all the delivered orders
        delivered_orders = PurchaseOrder.objects.filter(status="DELIVERED")

        # Randomly sample the orders
        sample_size = min(20, delivered_orders.count())
        selected_orders = random.sample(list(delivered_orders), sample_size)

        # Rate the orders
        for order in selected_orders:
            # Update the order details
            order.quality_rating = random.randint(1, 5)

            # Save the order
            order.save()


# Task to chain all tasks
@shared_task
def update_order_status():
    # Chain the tasks
    chain(
        issue_orders.s(),
        acknowledge_orders.s(),
        deliver_orders.s(),
        cancel_orders.s(),
        rate_orders.s(),
    ).apply_async()
