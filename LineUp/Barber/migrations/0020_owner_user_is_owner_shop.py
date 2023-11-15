<<<<<<< HEAD
# Generated by Django 4.2.6 on 2023-11-13 19:20
=======
# Generated by Django 4.2.7 on 2023-11-13 19:33
>>>>>>> c46e5d8 (Services form)

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
<<<<<<< HEAD
        ('Barber', '0019_service'),
=======
        ("Barber", "0019_service"),
>>>>>>> c46e5d8 (Services form)
    ]

    operations = [
        migrations.CreateModel(
<<<<<<< HEAD
            name='Owner',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='is_owner',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('barbers', models.ManyToManyField(related_name='shops', to='Barber.barber')),
                ('owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_shop', to='Barber.owner')),
=======
            name="Owner",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="is_owner",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="Shop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("address", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True)),
                ("slug", models.SlugField(blank=True, unique=True)),
                (
                    "barbers",
                    models.ManyToManyField(related_name="shops", to="Barber.barber"),
                ),
                (
                    "owner",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="owned_shop",
                        to="Barber.owner",
                    ),
                ),
>>>>>>> c46e5d8 (Services form)
            ],
        ),
    ]
