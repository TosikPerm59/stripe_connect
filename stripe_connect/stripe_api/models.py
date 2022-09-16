from django.db import models

class Item(models.Model):

    currency = {
        'usd': 'usd',
        'rub': 'rub'
    }
    name = models.CharField(max_length=30, verbose_name='Название товара')
    description = models.CharField(max_length=100, verbose_name='Описание', blank=True, name=True)
    currency = models.CharField(max_length=3, verbose_name='Валюта', choices=currency)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']


class Order(models.Model):
    session = models.CharField(max_length=30, verbose_name='Сессия')
    basket = models.CharField(max_length=100, verbose_name='Корзина', null=True, blank=True)
