import stripe

from .models import Order


def get_or_create_session_key(request_session):

    session_key = request_session.session_key

    if not session_key:
        request_session.create()
        request_session['basket'] = []
    else:
        if 'basket' not in request_session.keys():
            request_session['basket'] = []

    request_session.save()

    return session_key


def payment_intent_create(amount, currency):
    stripe.api_key = 'sk_test_51LgWe1IcEHFmfMmMy3TylDyqK3YSwRXbSbfpRfSPmr'
    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        payment_method_types=['card'],
    )

    return payment_intent


def get_item_id(request):
    try:
        item_id = request.GET.get('item_id')
        return item_id
    except:
        return None


def get_order(session_key):
    try:
        order = Order.objects.get(session_key=session_key)
        return order
    except:
        return None
