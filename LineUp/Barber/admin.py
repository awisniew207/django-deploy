from django.contrib import admin

from .models import *
'''
admin.site.register(Barber)
admin.site.register(Customer)
admin.site.register(Shop)
admin.site.register(Event)
admin.site.register(Service)
admin.site.register(EventService)
admin.site.register(Review)
admin.site.register(BarberUser)
'''
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['barber', 'start_time', 'end_time', 'is_booked']  # Adjust fields as needed
    
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Barber)
<<<<<<< HEAD
admin.site.register(TimeSlot) 
=======
admin.site.register(Owner)
>>>>>>> 8b550e4980fc3e83f1e4e45831b01760f6891f8c
