from django_cron import CronJobBase, Schedule
from .models import Barber, create_or_update_timeslots_for_barber, TimeSlot
from django.utils import timezone

class UpdateBarberTimeslotsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # run once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Barber.update_barber_timeslots'  # a unique code

    def do(self):
        for barber in Barber.objects.all():
            create_or_update_timeslots_for_barber(barber)


class ClearPastTimeSlotsCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # run daily

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Barber.clear_past_timeslots'  # a unique code

    def do(self):
        TimeSlot.objects.filter(end_time__lt=timezone.now()).delete()