# Generated by Django 4.2.6 on 2023-11-13 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Barber", "0017_alter_review_rating"),
    ]

    operations = [
        migrations.CreateModel(
            name="TimeSlot",
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
                ("start_time", models.DateTimeField()),
                ("end_time", models.DateTimeField()),
                ("is_booked", models.BooleanField(default=False)),
                (
                    "barber",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Barber.barber"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Appointment",
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
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "timeslot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Barber.timeslot",
                    ),
                ),
            ],
        ),
    ]
