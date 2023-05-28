from __future__ import unicode_literals
from django.contrib.gis.db import models
from colorfield.fields import ColorField
from django.shortcuts import reverse


class Streets(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'
        ordering = ['name']


class Points(models.Model):
    street = models.ForeignKey(Streets, null=True, on_delete=models.SET_NULL, verbose_name='улица')
    number = models.CharField(max_length=10, null=True, blank=False, verbose_name='номер дома/помещения')
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='доп. информация')
    points = models.PointField(srid=4326, null=True, blank=True, verbose_name='точка')

    with_circle = models.BooleanField(default=False, verbose_name='с радиусом БСПД')

    class Meta:
        verbose_name = 'Точка'
        verbose_name_plural = 'Точки'

    def __str__(self):
        return self.street.name + ', '+ self.number


class Lines(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.TextField(null=True, blank=True, verbose_name='описание')
    lines = models.MultiLineStringField(srid=4326, null=True, blank=True, verbose_name='линия')
    color = ColorField(default='#FF0000', null=True, blank=True, verbose_name='цвет линии')

    class Meta:
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'

    def __str__(self):
        return self.name


class ClientGroups(models.Model):
    name = models.CharField(max_length=100, verbose_name='название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы клиентов'


class Client(models.Model):
    group = models.ForeignKey(ClientGroups, null=True, on_delete=models.SET_NULL, verbose_name='группа')
    name = models.CharField(max_length=100, verbose_name='краткое наименование')
    full_name = models.CharField(max_length=500, default='-', verbose_name='полное наименование')

    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name='контактный телефон')

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('inforium:client_detail', kwargs={'client_id': self.id})

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['name']


class Equipment(models.Model):
    name = models.CharField(max_length=500, verbose_name='наименование')
    inv_number = models.CharField(max_length=9, verbose_name='инвентарный номер')
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL, verbose_name='клиент')

    def __str__(self):
        return self.name + ' - ' + self.inv_number

    class Meta:
        verbose_name = 'Оборудование'
        verbose_name_plural = 'Оборудование'


class Speed(models.Model):
    name = models.CharField(max_length=10, verbose_name='скорость канала')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Скорость каналов'
        verbose_name_plural = 'Скорость каналов'


class Instance(models.Model):
    port_type_choice = (
        ('Обл.', 'Областной'),
        ('Респ.', 'Республиканский')
    )

    service_type_choice = (
        ('БСПД', 'БСПД'),
        ('Спутник', 'Спутниковый канал'),
        ('Наземный', 'ВОЛС/DSL/ADSL/xDSL')
    )

    is_my = models.BooleanField(default=True, verbose_name='собственный договор')
    is_active = models.BooleanField(default=True, verbose_name='активный')
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL, verbose_name='клиент')

    service_type = models.CharField(max_length=20, default='Наземный', choices=service_type_choice, verbose_name='тип канала')
    port_type = models.CharField(max_length=20, default='Обл.', choices=port_type_choice, verbose_name='тип порта')

    point = models.ForeignKey(Points, null=True, on_delete=models.SET_NULL, verbose_name='точка')
    speed = models.ForeignKey(Speed, null=True, on_delete=models.SET_NULL, verbose_name='скорость канала')
    lan = models.GenericIPAddressField(protocol='IPv4', verbose_name='ip адрес сети')
    lan_mask = models.SmallIntegerField(default=24, verbose_name='маска подсети')

    def __str__(self):
        return self.client.name + ' --> ' + str(self.point)
    class Meta:
        verbose_name = 'Подключение'
        verbose_name_plural = 'Подключения'
