# Generated by Django 4.2.6 on 2023-11-25 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Barber', '0028_merge_20231125_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='booked_by',
        ),
        migrations.AddField(
            model_name='shop',
            name='affiliation_code',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='phone_number',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='barbers',
            field=models.ManyToManyField(blank=True, related_name='shops', to='Barber.barber'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_shops', to='Barber.owner'),
        ),
    ]
