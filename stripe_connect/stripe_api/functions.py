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

