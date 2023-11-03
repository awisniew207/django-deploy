# Generated by Django 4.2.6 on 2023-10-25 19:47

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0007_user_phone_num_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='profileView', editable=False, populate_from=['username', 'id'], unique=True),
        ),
    ]