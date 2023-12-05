# Generated by Django 3.2.6 on 2021-11-03 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_pielist_sort_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='NutritionalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serving_size', models.IntegerField()),
                ('energy_di', models.IntegerField(default=8700)),
                ('energy', models.IntegerField()),
                ('protein_di', models.IntegerField(default=50)),
                ('protein', models.IntegerField()),
                ('fat_di', models.IntegerField(default=70)),
                ('fat', models.IntegerField()),
                ('carbohydrate_di', models.IntegerField(default=310)),
                ('carbohydrate', models.IntegerField()),
                ('sodium_di', models.IntegerField(default=2300)),
                ('sodium', models.IntegerField()),
                ('pie_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='main.pielist')),
            ],
        ),
    ]
