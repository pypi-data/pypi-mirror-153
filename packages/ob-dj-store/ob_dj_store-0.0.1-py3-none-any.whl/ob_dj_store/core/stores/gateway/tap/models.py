import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ob_dj_store.core.stores.gateway.tap.managers import TapPaymentManager

logger = logging.getLogger(__name__)


class TapPayment(models.Model):
    """TapPayment captures the payment from Tap"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        help_text=_(
            "Captured the User ID for both registered "
            "users and Guests (Every guest user has a user_id assigned by device_id)"
        ),
    )
    langid = models.CharField(
        max_length=10,
        help_text=_(
            "Capture language for debugging & analytical only purposes (ARA for Arabic & ENG for English)"
        ),
    )
    payment = models.OneToOneField(
        "stores.Payment",
        on_delete=models.CASCADE,
        help_text=_("Reference local payment transaction table"),
    )
    result = models.CharField(
        max_length=100, help_text=_("Status response from TAP gateway")
    )
    # payment details
    payment_url = models.CharField(
        max_length=250, help_text=_("Captures generated URL for user payment")
    )
    charge_id = models.CharField(
        max_length=250,
        help_text=_("Charge ID returned from TAP"),
        unique=True,
        db_index=True,
    )
    init_response = models.JSONField(
        help_text=_("Response received when initiating the payment"),
        null=True,
        blank=True,
    )
    callback_response = models.JSONField(
        help_text=_("Callback response received after the payment is done"),
        null=True,
        blank=True,
    )
    # audit fields
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        help_text=_("Datetime when payment was initiated"),
    )
    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    objects = TapPaymentManager()

    class Meta:
        verbose_name = _("TAP Payment")
