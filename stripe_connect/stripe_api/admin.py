from django.contrib import admin
from models import Item, Order


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'currency', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('session', 'basket')


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
