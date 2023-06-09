# Generated by Django 3.1.6 on 2021-02-24 10:25

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitmap', '0024_auto_20210219_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instance',
            name='lan_mask',
            field=models.SmallIntegerField(default=24, verbose_name='маска подсети'),
        ),
        migrations.AlterField(
            model_name='lines',
            name='lines',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(blank=True, null=True, srid=4326, verbose_name='линия'),
        ),
    ]
