# Generated by Django 3.2.6 on 2021-11-03 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_nutritionalinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pielist',
            name='ingredients',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
