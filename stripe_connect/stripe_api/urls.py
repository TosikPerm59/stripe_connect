from django.contrib import admin
from django.urls import path

from .views import show_item, stripe_payment_intent, add_to_basket, basket, show_all_items

urlpatterns = [
    path('show_all_items/', show_all_items, name='show_all_items'),
    path('item/<int:item_id>/', show_item, name='show_item'),
    path('buy/', stripe_payment_intent, name='buy'),
    path('add/', add_to_basket, name='add'),
    path('basket/', basket, name='basket')
]
