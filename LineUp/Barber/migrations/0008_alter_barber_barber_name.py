# Generated by Django 4.2.6 on 2023-10-11 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0007_alter_review_barber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barber',
            name='barber_name',
            field=models.CharField(max_length=30),
        ),
    ]
