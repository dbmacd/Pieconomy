# Generated by Django 3.2.6 on 2021-11-03 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20211103_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bootstrapcolours',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
