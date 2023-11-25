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
import secrets
import string
import random
from django.urls import reverse

# User model
class User(AbstractUser):    
    is_customer = models.BooleanField(default=False)
    is_barber = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='uploads/', default='images/PIC_0102.JPG')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_num = models.CharField(max_length=12, blank=True)
    slug = AutoSlugField(populate_from='username', unique=True)

    def get_absolute_url(self):
        if self.is_customer:
            return reverse("customerProfileView", kwargs={"slug": self.slug})
        elif self.is_barber:
            return reverse("barberProfileView", kwargs={"slug": self.slug})
        elif self.is_owner:
            return reverse("ownerProfileView", kwargs={"slug": self.slug})

# Customer model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

# Barber model
class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    work_start_time = models.TimeField(default=time(9, 0))  # Default to 9:00 AM
    work_end_time = models.TimeField(default=time(17, 0))   # Default to 5:00 PM
    affiliation_code = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    def average_rating(self):
        reviews = self.barber_reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


# Owner model
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Additional fields for Owner if required

    def __str__(self):
        return self.user.username

# Shop model
def generate_affiliation_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=12)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name='owned_shops')
    affiliation_code = models.CharField(max_length=10, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    barbers = models.ManyToManyField('Barber', related_name='shops', blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Generate unique affiliation code and slug if not set
        if not self.affiliation_code:
            while True:
                code = generate_affiliation_code()
                if not Shop.objects.filter(affiliation_code=code).exists():
                    self.affiliation_code = code
                    break
        if not self.slug:
            self.slug = slugify(self.affiliation_code)
        super(Shop, self).save(*args, **kwargs)

    
class TimeSlot(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    booked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='booked_appointments')

    def __str__(self):
        return f"timeslot: {self.start_time} to {self.end_time}"

class Appointment(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)

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

def create_or_update_timeslots_for_barber(barber_instance):
    # Define the range of dates to generate timeslots for
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=7)

# Review model
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

# Service model
class Service(models.Model):
    barber = models.ForeignKey('Barber', on_delete=models.CASCADE, related_name='services', null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return f"{self.title} by {self.barber.user.username}" if self.barber else self.title
    

    
