# Generated by Django 4.2.6 on 2023-10-11 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0009_alter_barber_barber_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='review_title',
            field=models.CharField(default='Default', max_length=50),
        ),
    ]
