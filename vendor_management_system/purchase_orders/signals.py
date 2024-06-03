# Imports
from pprint import pprint

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from vendor_management_system.purchase_orders.models import PurchaseOrder
from vendor_management_system.purchase_orders.serializers import PurchaseOrderSerializer


# Create a signal to set the issue_date when a PurchaseOrder is issued
@receiver(pre_save, sender=PurchaseOrder)
def set_issue_date(sender, instance, **kwargs):
    try:
        # Get the initial state of the instance before saving
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    # Check if the status is changing from PENDING to ISSUED
    if old_instance.status == "PENDING" and instance.status == "ISSUED":
        # # * Set the issue_date to the current date
        # instance.issue_date = timezone.now().date()

        # ! Set the issue date to the date passed
        instance.issue_date = instance.issue_date


# Create a signal to set the acknowledgment_date when a PurchaseOrder is acknowledged
@receiver(pre_save, sender=PurchaseOrder)
def set_acknowledgment_date(sender, instance, **kwargs):
    try:
        # Get the initial state of the instance before saving
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    # Check if the status is changing from ISSUED to ACKNOWLEDGED
    if old_instance.status == "ISSUED" and instance.status == "ACKNOWLEDGED":
        # # * Set the acknowledgment_date to the current date
        # instance.acknowledgment_date = timezone.now().date()

        # ! Set the acknowledgment date to the date passed
        instance.acknowledgment_date = instance.acknowledgment_date


# Create a signal to set the actual_delivery_date when a PurchaseOrder is marked as DELIVERED
@receiver(pre_save, sender=PurchaseOrder)
def set_actual_delivery_date(sender, instance, **kwargs):
    try:
        # Get the initial state of the instance before saving
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    # Check if the status is changing from ACKNOWLEDGED to DELIVERED
    if old_instance.status == "ACKNOWLEDGED" and instance.status == "DELIVERED":
        # # * Set the actual_delivery_date to the current date
        # instance.actual_delivery_date = timezone.now().date()

        # ! Set the actual delivery date to the date passed
        instance.actual_delivery_date = instance.actual_delivery_date


# Create a signal to set the on_time_delivery_rate of the Vendor when a PurchaseOrder is marked as DELIVERED
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_on_time_delivery_rate(sender, instance, **kwargs):
    # Check if the instance is being updated (not created)
    if instance.status != "PENDING":
        # Get the vendor
        vendor = instance.vendor

        # Get the list of all completed deliveries by the Vendor
        completed_deliveries = PurchaseOrder.objects.filter(
            vendor=vendor, status="DELIVERED"
        )

        # Get the all the PurchaseOrders delivered on time by the Vendor
        on_time_delivers_orders = completed_deliveries.filter(
            actual_delivery_date__lte=models.F("expected_delivery_date")
        )

        if completed_deliveries.count() > 0:
            # Calculate the on_time_delivery_rate
            on_time_delivery_rate = (
                on_time_delivers_orders.count() / completed_deliveries.count()
            )

            # Update the on_time_delivery_rate of the Vendor
            vendor.on_time_delivery_rate = round(on_time_delivery_rate * 100, 4)

            # Save the Vendor
            vendor.save()


# Create a signal to set the quality_rating_avg of the Vendor when a PurchaseOrder is marked as DELIVERED and is rated
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_quality_rating_avg(sender, instance, **kwargs):
    # Check if the instance is being updated (not created)
    if instance.status not in ["PENDING", "CANCELLED"] and instance.vendor is not None:

        # Get the vendor
        vendor = instance.vendor

        # If the vendor.quality_rating_avg is not None
        if vendor.quality_rating_avg is not None:
            # Check if current order is rated
            if instance.quality_rating is not None:
                # Calculate the quality_rating_avg
                quality_rating_avg = (
                    vendor.quality_rating_avg + instance.quality_rating
                ) / 2

                # Update the quality_rating_avg of the Vendor
                vendor.quality_rating_avg = quality_rating_avg

                # Save the Vendor
                vendor.save()

        else:
            # Get the list of all rated PurchaseOrders by the Vendor
            rated_orders = PurchaseOrder.objects.filter(
                vendor=vendor, status="DELIVERED", quality_rating__isnull=False
            )

            if rated_orders.count() > 0:
                # Calculate the quality_rating_avg
                quality_rating_avg = rated_orders.aggregate(
                    avg_quality_rating=models.Avg("quality_rating")
                )["avg_quality_rating"]

                # Update the quality_rating_avg of the Vendor
                vendor.quality_rating_avg = round(quality_rating_avg, 4)

                # Save the Vendor
                vendor.save()


# Create a signal to set the average_response_time of the Vendor when a PurchaseOrder is marked as ACKNOWLEDGED
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_average_response_time(sender, instance, **kwargs):
    # Check if the instance is being updated (not created)
    if instance.status != "PENDING":
        # Get the vendor
        vendor = instance.vendor

        # Get the list of all acknowledged PurchaseOrders by the Vendor
        acknowledged_orders = PurchaseOrder.objects.filter(
            vendor=vendor, status="ACKNOWLEDGED"
        )

        if acknowledged_orders.count() > 0:
            # Calculate the average_response_time
            total_response_time = sum(
                (
                    (order.acknowledgment_date - order.issue_date).total_seconds()
                    / 3600
                    for order in acknowledged_orders
                )
            )
            average_response_time = total_response_time / acknowledged_orders.count()

            # Update the average_response_time of the Vendor
            vendor.average_response_time = round(average_response_time, 4)

            # Save the Vendor
            vendor.save()


# Create a signal to set the fulfillment_rate of the Vendor when a PurchaseOrder is marked as DELIVERED
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_fulfillment_rate(sender, instance, **kwargs):
    # Check if the instance being updated (not created)
    if instance.status != "PENDING":
        # Get the vendor
        vendor = instance.vendor

        # Get the list of all completed deliveries by the Vendor
        completed_deliveries = PurchaseOrder.objects.filter(
            vendor=vendor, status="DELIVERED"
        )

        # Issued orders
        issued_orders = PurchaseOrder.objects.filter(
            vendor=vendor, issue_date__isnull=False
        )

        if issued_orders.count() > 0:
            # Calculate the fulfillment_rate
            fulfillment_rate = completed_deliveries.count() / issued_orders.count()

            # Update the fulfillment_rate of the Vendor
            vendor.fulfillment_rate = round(fulfillment_rate * 100, 4)

            # Save the Vendor
            vendor.save()
