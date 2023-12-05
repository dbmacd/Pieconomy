# Generated by Django 3.2.6 on 2021-11-04 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_pielist_ingredients'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pieheaders',
            name='blurb_text',
        ),
        migrations.RemoveField(
            model_name='pieheaders',
            name='heading_text',
        ),
        migrations.RemoveField(
            model_name='pieheaders',
            name='image_alt_text',
        ),
        migrations.RemoveField(
            model_name='pieheaders',
            name='image_url',
        ),
        migrations.AddField(
            model_name='pieheaders',
            name='pie_data',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='main.pielist'),
            preserve_default=False,
        ),
    ]
