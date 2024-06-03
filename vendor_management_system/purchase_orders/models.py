# Imports
import uuid

from django.core import validators
from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Model for PurchaseOrder
class PurchaseOrder(models.Model):
    # Fields
    po_number = models.CharField(
        _("Purchase Order Number"),
        max_length=10,
        unique=True,
        primary_key=True,
        editable=False,
        help_text=_("Unique Purchase Order Number"),
        validators=[
            validators.RegexValidator(
                regex=r"^[A-Z0-9]+$",
                message=_("Purchase Order Number must be uppercase alphanumeric"),
            )
        ],
    )
    vendor = models.ForeignKey(
        "vendors.Vendor",
        on_delete=models.SET_NULL,
        verbose_name=_("Vendor"),
        help_text=_("Vendor associated with Purchase Order"),
        null=True,
        blank=True,
    )
    order_date = models.DateTimeField(
        _("Order Date"),
        help_text=_("Date of Purchase Order"),
        default=timezone.now,
    )
    expected_delivery_date = models.DateTimeField(
        _("Expected Delivery Date"),
        help_text=_("Expected Date of Delivery"),
        null=True,
        blank=True,
    )
    actual_delivery_date = models.DateTimeField(
        _("Actual Delivery Date"),
        help_text=_("Actual Date of Delivery"),
        null=True,
        blank=True,
    )
    items = models.JSONField(
        _("Items"), help_text=_("Items in Purchase Order"), null=False, blank=False
    )
    quantity = models.IntegerField(
        _("Quantity"),
        help_text=_("Total Quantity in Purchase Order"),
        validators=[validators.MinValueValidator(1)],
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=[
            ("PENDING", _("Pending")),
            ("ISSUED", _("Issued")),
            ("ACKNOWLEDGED", _("Acknowledged")),
            ("DELIVERED", _("Delivered")),
            ("CANCELLED", _("Cancelled")),
        ],
        default="PENDING",
        help_text=_("Status of Purchase Order"),
    )
    quality_rating = models.FloatField(
        _("Quality Rating"),
        max_length=1,
        choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
        null=True,
        blank=True,
        help_text=_("Quality Rating of Purchase Order"),
    )
    issue_date = models.DateTimeField(
        _("Issue Date"), help_text=_("Date of Issue"), null=True, blank=True
    )
    acknowledgment_date = models.DateTimeField(
        _("Acknowledgment Date"),
        help_text=_("Date of Acknowledgment"),
        null=True,
        blank=True,
    )

    # Metadata
    class Meta:
        verbose_name = _("Purchase Order")
        verbose_name_plural = _("Purchase Orders")
        ordering = ["order_date"]

    # String representation
    def __str__(self):
        return self.po_number

    # Save method
    def save(self, *args, **kwargs):
        # If purchase order number is not specified
        if not self.po_number:
            # Generate a new purchase order number
            self.po_number = str(uuid.uuid4()).replace("-", "")[:10].upper()

        # If the expected delivery date is not specified
        if not self.expected_delivery_date:
            # Calculate the expected delivery date
            self.expected_delivery_date = self.order_date + timezone.timedelta(days=21)

        # Save the model
        super(PurchaseOrder, self).save(*args, **kwargs)
