# Generated by Django 3.1.6 on 2021-02-17 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nitmap', '0017_delete_polygons'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='instance',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
