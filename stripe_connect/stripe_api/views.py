import stripe
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Item, Order
from .functions import get_or_create_session_key, get_item_id, get_order


def show_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'stripe_api/show_item.html', {'item': item})


def show_all_items(request):
    items = Item.objects.all()

    return render(request, 'stripe_api/show_all_items.html', {'items': items})


def basket(request):
    session_key = get_or_create_session_key(request.session)
    order = get_order(session_key)
    different_currency = False
    currency_set = set()

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
            item = Item.objects.get(id=item_id)
            currency_set.add(item.currency)
            items.append(item)

        if len(currency_set) > 1:
            different_currency = True

        context = {
            'items': items,
            'different_currency': different_currency
        }

        return render(request, 'stripe_api/basket.html', context=context)


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
    item, currency, line_items = None, None, []
    stripe.api_key = 'sk_test_51LgWe1IcEHFmfMmMy3TylDyqK3YSwRXbSbfpRfSPmr0R6S1KZo09gDvg9Zk1ubrFxxG8GYP6dxxr1Cekp1kRvs0c004HDP1L5O'
    item_id = get_item_id(request)


    if item_id:
        item = Item.objects.get(id=item_id)
        line_items = [{
                        'price_data': {
                                        'currency': item.currency,
                                        'product_data': {'name': item.name},
                                        'unit_amount': int(item.price * 100),
                                        },
                        'quantity': 1,
                        }]
    else:
        items_id = request.session['basket']
        session_key = get_or_create_session_key(request.session)
        try:
            currency = request.GET.get('currency_radio')
        except:
            pass

        for item_id in items_id:
            item = Item.objects.get(id=item_id)
            if currency:
                if item.currency != currency:
                    if item.currency == 'rub':
                        item.price = item.price / 60
                        item.currency = currency
                    else:
                        item.price = item.price * 60
                        item.currency = currency
            line_item = {
                        'price_data': {
                                        'currency': item.currency,
                                        'product_data': {'name': item.name},
                                        'unit_amount': int(item.price * 100),
                                        },
                        'quantity': 1,
                        }
            line_items.append(line_item)

    session = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )

    order = get_order(session_key)
    order.user_basket = []
    order.save()

    return redirect(session.url, code=303)



