from django.db import models

class Barber(models.Model):
    barber_name = models.CharField(max_length=30)
    reviews = models.IntegerField(default=0)

