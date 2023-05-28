# Generated by Django 3.1.6 on 2021-02-09 11:49

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitmap', '0008_auto_20210209_1749'),
    ]

    operations = [
        migrations.AddField(
            model_name='polygons',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='polygons',
            name='points',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
    ]