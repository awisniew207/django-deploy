# Generated by Django 4.2.6 on 2023-11-13 05:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0017_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='barber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barber_reviews', to='Barber.barber'),
        ),
        migrations.AlterField(
            model_name='review',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_reviews', to=settings.AUTH_USER_MODEL),
        ),
    ]
