from django.db import models


class Item(models.Model):

    def __str__(self):
        return self.name

    currency = (
        ('usd', 'usd'),
        ('rub', 'rub')
    )

    name = models.CharField(max_length=30, verbose_name='Название товара')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    currency = models.CharField(max_length=3, verbose_name='Валюта', choices=currency, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена', blank=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']


class Order(models.Model):
    session_key = models.CharField(max_length=30, verbose_name='Сессия')
    user_basket = models.CharField(max_length=100, verbose_name='Корзина для сессии', null=True, blank=True)

    class Meta:
        verbose_name = 'Корзина для сессии'
        verbose_name_plural = 'Корзины'
