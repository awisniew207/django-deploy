from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from autoslug import AutoSlugField
from django.utils.text import slugify
User = settings.AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, datetime, time
from django.db.models import TimeField
from django.urls import reverse

class User(AbstractUser):    
    is_customer = models.BooleanField(default=False)
    is_barber = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='uploads/', default='images/PIC_0102.JPG')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_num = models.CharField(max_length=12, blank=True)
    slug = AutoSlugField(populate_from='generate_slug', null=False, unique=True)
    works = [models.ImageField(upload_to='uploads/', default='images/PIC_0102.JPG'), 
            models.ImageField(upload_to='uploads/', default='images/PIC_0102.JPG'), 
            models.ImageField(upload_to='uploads/', default='images/PIC_0102.JPG')]

    def generate_slug(self):
        return slugify(f'{self.username}')

    def get_absolute_url(self):
        if self.user.is_customer:
            return reverse("customerProfileView", kwargs={"slug": self.slug})
        if self.user.is_barber:
            return reverse("barberProfileView", kwargs={"slug": self.slug})

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_customer = True

    def __str__(self):
        return self.user.username

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_barber = True
    work_start_time = TimeField(default=time(9, 0))  # Default to 9:00 AM
    work_end_time = TimeField(default=time(17, 0))   # Default to 5:00 PM

    def __str__(self):
        return self.user.username

class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_owner = True

    def __str__(self):
        return self.user.username

class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_reviews')
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='barber_reviews')
    content = models.TextField()
    RATING_CHOICES = [
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer.username} for {self.barber.user.username}"
    
class TimeSlot(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

class Appointment(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)


'''
@receiver(post_save, sender=Barber)
def create_timeslots_for_barber(sender, instance, created, **kwargs):
    if created:
        start_date = timezone.now().date()
        for day_delta in range(7):  # Adjust as needed
            day = start_date + timedelta(days=day_delta)
            start_datetime = timezone.make_aware(datetime.combine(day, instance.work_start_time))
            end_datetime = timezone.make_aware(datetime.combine(day, instance.work_end_time))

            current_time = start_datetime
            while current_time < end_datetime:
                timeslot_end = current_time + timedelta(hours=1)
                TimeSlot.objects.get_or_create(barber=instance, start_time=current_time, end_time=timeslot_end)
                current_time = timeslot_end
'''

def create_or_update_timeslots_for_barber(barber_instance):
    # Clear existing future timeslots for the barber
    TimeSlot.objects.filter(barber=barber_instance, start_time__gt=timezone.now()).delete()

    # Generate new timeslots
    work_start_hour = barber_instance.work_start_time.hour
    work_end_hour = barber_instance.work_end_time.hour

    start_date = timezone.now().date()
    for day_delta in range(7):  # Adjust as needed
        day = start_date + timedelta(days=day_delta)

        for hour in range(work_start_hour, work_end_hour):
            start_time = timezone.make_aware(datetime.combine(day, time(hour, 0)))
            end_time = start_time + timedelta(hours=1)  # 1-hour duration
            TimeSlot.objects.create(barber=barber_instance, start_time=start_time, end_time=end_time)



class Service(models.Model):
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, related_name='services', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return f"{self.title} by {self.barber.user.username}" if self.barber else self.title
    

class Shop(models.Model):
    name = models.CharField(max_length=100)
    owner = models.OneToOneField(Owner, on_delete=models.SET_NULL, null=True, related_name='owned_shop')
    barbers = models.ManyToManyField(Barber, related_name='shops')
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Shop, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
