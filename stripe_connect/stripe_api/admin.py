from django.contrib import admin
from .models import Item, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'currency')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'user_basket')


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
