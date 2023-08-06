import logging

from django.db import models

from ob_dj_store.core.stores.gateway.tap import utils

logger = logging.getLogger(__name__)


class TapPaymentManager(models.Manager):
    def create(self, **kwargs):
        # TODO: Add logging to on debug level
        payment = kwargs.get("payment")
        charge_id, payment_url, init_response = utils.initiate_payment(
            payment.order, payment, payment.currency
        )
        kwargs["charge_id"] = charge_id
        kwargs["payment_url"] = payment_url
        kwargs["init_response"] = init_response
        instance = super(TapPaymentManager, self).create(**kwargs)
        return instance
