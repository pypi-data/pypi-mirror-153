import logging

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from ob_dj_store.core.stores.managers import PaymentManager

logger = logging.getLogger(__name__)


class Payment(models.Model):
    """Payment captures the order payment either COD or via a Gateway"""

    class Gateway(models.TextChoices):
        COD = "cod"
        TAP = "tap"

    class PaymentStatus(models.TextChoices):
        INIT = "INIT"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"
        ERROR = "ERROR"

    status = models.CharField(
        max_length=100,
        default=PaymentStatus.INIT,
        choices=PaymentStatus.choices,
    )
    gateway = models.CharField(max_length=40, choices=Gateway.choices)
    gateway_ref_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text=_("A reference (Primary key) of the gateway transaction table"),
    )
    order = models.OneToOneField("stores.Order", on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    currency = models.CharField(_("Currency"), max_length=10)
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    payment_post_at = models.DateTimeField(_("Payment Post At"), null=True, blank=True)

    objects = PaymentManager()

    class Meta:
        ordering = ["-created_at"]
