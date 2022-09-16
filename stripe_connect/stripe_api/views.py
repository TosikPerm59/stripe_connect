from django.shortcuts import render
from django.http import HttpResponse

from .models import Item, Order


def basket(request):
    if 'basket' not in request.session.keys():
        return HttpResponse('Ваша корзина пуста')
    else:
        item_id_list = request.session['basket']
        items = []
        if item_id_list is None:
            return HttpResponse('Ваша корзина пуста')
        else:
            for item_id in item_id_list:
                items.append(Item.objects.get(id=item_id))
        return render(request, )


    # order = None
    # if request.method == 'GET':
    #     item_id = request.GET.get('item_id')
    #     items = Item.objects.get(id='item_id')
    # else:
    #     if order:
    #         pass


def show_item(request, item_id):
    item = Item.objects.get(id=item_id)
    print(type(item))
    return render(request, 'stripe_api/show_item.html', {'item': item})


def stripe_payment_intent(request):
    pass


def add_to_basket(request):
    item_id = request.GET.get('item_id')
    item = Item.objects.get(id=item_id)
    print(request.session.keys())
    if 'basket' not in request.session.keys():
        print('BASKET')
        request.session['basket'] = [set()]
        if item_id not in request.session['basket']:
            request.session['basket'].append(item_id)
    else:
        print('NONE')

        if item_id not in request.session['basket']:
            print('item_id not in request.session[basket]')
            request.session['basket'].append(item_id)
    request.session.save()
    print(request.session['basket'])
    return render(request, 'stripe_api/show_item.html', {'item': item})
