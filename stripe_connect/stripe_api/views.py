from django.contrib.auth import login
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import Item, Order


def show_all_items(request):
    items = Item.objects.all()

    return render(request, 'stripe_api/show_all_items.html', {'items': items})


def basket(request):
    order = None
    session_key = request.session.session_key
    if session_key:

        try:
            order = Order.objects.get(session_key=session_key)
        except:
            pass

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
        if item_id_list is None:
            return HttpResponse('Ваша корзина пуста')
        else:
            for item_id in item_id_list:
                items.append(Item.objects.get(id=item_id))
        return render(request, 'stripe_api/basket.html', {'items': items})


def show_item(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'stripe_api/show_item.html', {'item': item})


def stripe_payment_intent(request):
    pass


def add_to_basket(request):
    item_id, order, item = None, None, None
    session_key = request.session.session_key


    if not session_key:
        request.session.create()
        request.session['basket'] = []
        request.session.save()
    else:
        if 'basket' not in request.session.keys():
            request.session['basket'] = []

    try:
        order = Order.objects.get(session_key=session_key)
    except:
        pass

    if not order:
        order = Order()
        order.session_key = session_key
        order.user_basket = request.session['basket']

    try:
        item_id = request.GET.get('item_id')
    except:
        pass

    if item_id:
        if item_id not in request.session['basket']:
            request.session['basket'].append(item_id)
            request.session.save()
            order.user_basket = request.session['basket']
            order.save()
        item = Item.objects.get(id=item_id)

    return render(request, 'stripe_api/show_item.html', {'item': item})
