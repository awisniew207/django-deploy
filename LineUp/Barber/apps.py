from django.apps import AppConfig


class BarberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Barber'

class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Customer'
