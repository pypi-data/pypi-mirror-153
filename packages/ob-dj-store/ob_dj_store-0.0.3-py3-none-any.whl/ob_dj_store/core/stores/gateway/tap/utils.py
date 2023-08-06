from ob_dj_store.core.stores.models import Order, Payment


def initiate_payment(order: Order, payment: Payment, currency_code: str):
    """Initiate payment URL and return charge_id, payment_url and response"""
    return "charge-id", "payment-url", {"status": "success"}
