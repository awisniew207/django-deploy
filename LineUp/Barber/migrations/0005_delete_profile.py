# Generated by Django 4.2.6 on 2023-10-23 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0004_alter_user_profile_pic_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]