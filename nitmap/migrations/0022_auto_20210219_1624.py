# Generated by Django 3.1.6 on 2021-02-19 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitmap', '0021_auto_20210219_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='streets',
            options={'ordering': ['name'], 'verbose_name': 'Улица', 'verbose_name_plural': 'Улицы'},
        ),
        migrations.AlterField(
            model_name='client',
            name='phone',
            field=models.CharField(max_length=100, null=True, verbose_name='контактный телефон'),
        ),
    ]
