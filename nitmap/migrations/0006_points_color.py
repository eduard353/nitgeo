# Generated by Django 3.1.6 on 2021-02-09 10:08

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nitmap', '0005_auto_20210208_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='points',
            name='color',
            field=colorfield.fields.ColorField(blank=True, default='#FF0000', max_length=18, null=True),
        ),
    ]
