# Imports
import uuid

from django.core import validators
from django.db import models
from django.utils.translation import gettext_lazy as _


# Model for Vendor
class Vendor(models.Model):
    # Fields
    vendor_code = models.CharField(
        _("Vendor Code"),
        max_length=10,
        unique=True,
        primary_key=True,
        editable=False,
        help_text=_("Unique code for Vendor"),
        validators=[
            validators.RegexValidator(
                regex=r"^[A-Z0-9]+$",
                message=_("Vendor Code must be uppercase alphanumeric"),
            )
        ],
    )
    name = models.CharField(
        _("Name of Vendor"), max_length=255, help_text=_("Name of Vendor")
    )
    contact_details = models.TextField(
        _("Contact Details of Vendor"), help_text=_("Contact Details of Vendor")
    )
    address = models.TextField(_("Address of Vendor"), help_text=_("Address of Vendor"))
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
        help_text=_("Average Response Time of Vendor in Hours"),
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
        verbose_name = _("Vendor")
        verbose_name_plural = _("Vendors")
        ordering = ["name"]

    # String representation
    def __str__(self):
        return self.name

    # Save method
    def save(self, *args, **kwargs):
        # If vendor code is not specified
        if not self.vendor_code:
            # Generate a new vendor code
            self.vendor_code = str(uuid.uuid4()).replace("-", "")[:10].upper()

        # Save the model
        super(Vendor, self).save(*args, **kwargs)
