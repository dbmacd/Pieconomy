# Generated by Django 3.2.6 on 2021-11-10 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_orderitems_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='create_date_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='orders',
            name='last_updated_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
