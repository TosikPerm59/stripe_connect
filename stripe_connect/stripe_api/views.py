import stripe
from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Item, Order
from .functions import get_or_create_session_key, get_item_id, get_order, payment_intent_create


def show_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'stripe_api/show_item.html', {'item': item})


def show_all_items(request):
    items = Item.objects.all()

    return render(request, 'stripe_api/show_all_items.html', {'items': items})


def basket(request):
    session_key = get_or_create_session_key(request.session)
    order = get_order(session_key)

    if request.GET.get('to_do') == 'basket_clear':
        request.session['basket'] = []
        request.session.save()
        if order:
            order.user_basket = []
            order.save()
        return HttpResponse('Ваша корзина очищена')

    if 'basket' not in request.session.keys() or request.session['basket'] == []:
        return HttpResponse('Ваша корзина пуста')

    else:
        item_id_list = request.session['basket']
        items = []

        for item_id in item_id_list:
            items.append(Item.objects.get(id=item_id))

        return render(request, 'stripe_api/basket.html', {'items': items})


def add_to_basket(request):
    item = None
    session_key = get_or_create_session_key(request.session)
    item_id = get_item_id(request)
    order = get_order(session_key)

    if not order:
        order = Order()
        order.session_key = session_key
        order.user_basket = request.session['basket']

    if item_id:
        if item_id not in request.session['basket']:
            request.session['basket'].append(item_id)
            request.session.save()
            order.user_basket = request.session['basket']
            order.save()
        item = Item.objects.get(id=item_id)

    return render(request, 'stripe_api/show_item.html', {'item': item})


def buy(request):
    item = None
    item_id = get_item_id(request)
    session_key = get_or_create_session_key(request.session)

    if item_id:
        item = Item.objects.get(id=item_id)

    if 'paiment_intent' not in request.session.keys():
        payment_intent = payment_intent_create(item.price, item.currency)
        request.session['payment_intent'] = payment_intent


