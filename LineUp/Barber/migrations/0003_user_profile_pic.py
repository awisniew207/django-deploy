# Generated by Django 4.2.6 on 2023-10-23 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0002_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
