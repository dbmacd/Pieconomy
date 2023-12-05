# Generated by Django 3.2.6 on 2021-11-02 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20211102_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='PieHeaders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(upload_to='')),
                ('image_alt_text', models.TextField()),
                ('heading_text', models.TextField(max_length=50)),
                ('blurb_text', models.TextField(max_length=100)),
                ('button_text', models.TextField(max_length=20)),
                ('button_link', models.TextField()),
                ('show_on_header', models.BooleanField()),
                ('heading_text_style', models.TextField(default='text-dark')),
                ('blurb_text_style', models.TextField(default='text-dark')),
                ('button_style', models.TextField(default='btn-primary')),
            ],
        ),
        migrations.AlterField(
            model_name='carouselitems',
            name='button_style',
            field=models.TextField(default='btn-primary'),
        ),
    ]
