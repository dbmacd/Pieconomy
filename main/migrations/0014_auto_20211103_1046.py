# Generated by Django 3.2.6 on 2021-11-03 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20211103_1000'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='pielist',
            name='allergens',
            field=models.ManyToManyField(to='main.Allergens'),
        ),
    ]
