# Generated by Django 3.1.6 on 2021-02-03 15:35

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitmap', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='second',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='second',
            name='polygons',
            field=django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326),
        ),
    ]
