# Imports
import uuid

from django.core import validators
from django.db import models

from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Model for HistoricalPerformance
class HistoricalPerformance(models.Model):
    # Fields
    id = models.CharField(
        _("Historical Performance Record ID"),
        max_length=10,
        unique=True,
        primary_key=True,
        editable=False,
        help_text=_("Unique ID for Historical Performance Record"),
        validators=[
            validators.RegexValidator(
                regex=r"^[A-Z0-9]+$",
                message=_("ID must be uppercase alphanumeric"),
            )
        ],
    )
    vendor = models.ForeignKey(
        "vendors.Vendor",
        on_delete=models.CASCADE,
        verbose_name=_("Vendor"),
        help_text=_("Vendor associated with Purchase Order"),
    )
    date = models.DateTimeField(
        _("Date"),
        help_text=_("Date of Historical Performance Record"),
        default=timezone.now,
    )
    on_time_delivery_rate = models.FloatField(
        _("On-time Delivery Rate"),
        help_text=_("On-time Delivery Rate of Vendor"),
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
        null=True,
        blank=True,
    )
    quality_rating_avg = models.FloatField(
        _("Quality Rating Average"),
        help_text=_("Quality Rating Average of Vendor"),
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)],
        null=True,
        blank=True,
    )
    average_response_time = models.FloatField(
        _("Average Response Time"),
        help_text=_("Average Response Time of Vendor"),
        validators=[validators.MinValueValidator(0)],
        null=True,
        blank=True,
    )
    fulfillment_rate = models.FloatField(
        _("Fulfillment Rate"),
        help_text=_("Fulfillment Rate of Vendor"),
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)],
        null=True,
        blank=True,
    )

    # Metadata
    class Meta:
        verbose_name = _("Historical Performance")
        verbose_name_plural = _("Historical Performances")
        ordering = ["-date"]

    # String representation
    def __str__(self):
        return f"{self.vendor} - {self.date}"

    # Save method
    def save(self, *args, **kwargs):
        # If id is not specified
        if not self.id:
            # Generate a new id
            self.id = str(uuid.uuid4()).replace("-", "")[:10].upper()

        # Save the model
        super(HistoricalPerformance, self).save(*args, **kwargs)
