# Generated by Django 4.2.6 on 2023-11-20 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0022_remove_shop_barbers_remove_shop_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='shop',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
    ]