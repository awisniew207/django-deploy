from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from autoslug import AutoSlugField
from django.utils.text import slugify
User = settings.AUTH_USER_MODEL
'''
class Shop(models.Model):
    affiliation_code = models.CharField(unique=True, max_length=20)                            # Each shop has this unique code, needed when creating 
    name = models.CharField(max_length=50)                                                   # Shop name, will be set by shop admin account 
    location = models.CharField(max_length=60, unique=True)                                    # Shop location, will be set by shop admin account 
    phone_num = models.CharField(blank=True, null=True, max_length=12)                         # Shop specific phone number, different than personal


class Barber(models.Model):
    # In any of these fields, adjust max_length as needed 
    username = models.CharField(max_length=30, unique=True, default="Username")                     # Needed when creating account 
    password = models.CharField(max_length=30, unique=True, default="Password")                         # Needed when creating account 
    f_name = models.CharField(max_length=30, blank=True, null=True)             # Set after account is created 
    l_name = models.CharField(max_length=30, blank=True, null=True)             # Set after account is created 
    email = models.CharField(max_length=30, unique=True, null=True)                        # Needed when creating account 
    is_owner = models.BooleanField(default=False)                                            # True if owner, False if just barber 
    profile_pic = models.ImageField(upload_to='images/', blank=True, null=True) # Can change file location and file type 
    phone_num = models.CharField(blank=True, null=True, max_length=12)                         # Barber personal phone number 
    #shop = models.ForeignKey(Shop, default="Independent",  on_delete=models.CASCADE)                    # Corresponding shop 

    def __str__(self):
        return self.barber_name

        
class Customer(models.Model):
    # In any of these fields, adjust max_length as needed 
    username = models.CharField(max_length=30, unique=True, default="Username")                     # Needed when creating account 
    password = models.CharField(max_length=30, unique=True, default="Password")                     # Needed when creating account 
    f_name = models.CharField(max_length=30, blank=True, null=True)             # Set after account is created 
    l_name = models.CharField(max_length=30, blank=True, null=True)             # Set after account is created 
    email = models.CharField(max_length=30, unique=True, null=True)                        # Needed when creating account 
    profile_pic = models.ImageField(upload_to='images/', blank=True, null=True) # Can change file location and file type 
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)                                          # Corresponding barber 
    
    def __str__(self):
        return f"{self.username}"

        
class Event(models.Model):
    date = models.DateField()                                                   # Needed when creating an Event 
    start_time = models.TimeField()                                             # Needed when creating an Event 
    end_time = models.TimeField()                                               # Needed when creating an Event  
    #barber = models.ForeignKey(Barber, blank=False, on_delete=models.CASCADE)                # Barbers 
    customer = models.ForeignKey(Customer, blank=False, on_delete=models.CASCADE)            # Customers


class Service(models.Model):
    title = models.CharField(max_length=40, unique=True, blank=True)                                                  # Title of service, needed when creating Service 
    description = models.TextField(blank=True, null=True)                       # Description of service 
    price = models.FloatField()                                                 # Price of service, needed when creating Service
    duration = models.IntegerField()                                            # Duration of service, needed when creating Service 
    #barber = models.ForeignKey(Barber, on_delete=models.CASCADE)                # Corresponding barber


class EventService(models.Model):
    # Events and services have a many to many relationship
    # Event can have multiple services (i.e. haircut, beard trim)
    # Service can have multiple events 
    event = models.ForeignKey(Event, on_delete=models.CASCADE)                                            # Events
    service = models.ForeignKey(Service, on_delete=models.CASCADE)                                        # Services 


class Review(models.Model):
    date = models.DateField(auto_now_add=True)                                  # Date of review, automatically sent to current date, needed when creating 
    rating = models.IntegerField()                                              # Rating of review, needed when creating 
    title = models.CharField(max_length=50, default="Review")                                     # Title of review, needed when creating 
    description = models.TextField()                                            # Description of review, needed when creating 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)            # Customer that set review 
    #barber = models.ForeignKey(Barber, blank=False, on_delete=models.CASCADE)                # Barber for review

    def __str__(self):
        return self.review_title
'''
#class Profile(models.Model):
 #   user = models.OneToOneField(User, on_delete=models.CASCADE)
    #fields = '__all__'

class User(AbstractUser):    
    is_customer = models.BooleanField(default=False)
    is_barber = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='uploads/', default='images/PIC_0102.JPG')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone_num = models.CharField(max_length=12, blank=True)
    slug = AutoSlugField(populate_from='generate_slug', null=False, unique=True)

    def generate_slug(self):
        return slugify(f'{self.username}')

    def get_absolute_url(self):
        return reverse("profileView", kwargs={"slug": self.slug})

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_customer = True

    def __str__(self):
        return self.user.username

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_barber = True

    def __str__(self):
        return self.user.username