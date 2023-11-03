# Generated by Django 4.2.6 on 2023-10-26 23:07

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0010_alter_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='generate_slug', unique=True),
        ),
    ]