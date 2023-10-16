from django.db import models

class Shop(models.Model):
    affiliation_code = models.CharField(unique=True)                            # Each shop has this unique code, needed when creating 
    name = models.CharField()                                                   # Shop name, will be set by shop admin account 
    location = models.CharField(unique=True)                                    # Shop location, will be set by shop admin account 
    phone_num = models.CharField(blank=True, null=True)                         # Shop specific phone number, different than personal

    # Functions to grad data, todo 


class Barber(models.Model):
    # In any of these fields, adjust max_length as needed 
    username = models.CharField(max_length=30, unique=True)                     # Needed when creating account 
    password = models.CharField(max_length=30, unique=True)                     # Needed when creating account 
    f_name = models.CharField(max_length=30, blank=True, null=True)             # Set after account is created 
    l_name = models.CharField(max_length=30, blank=True, null=True)             # Set after account is created 
    email = models.CharField(max_length=30, unique=True)                        # Needed when creating account 
    is_owner = models.BooleanField()                                            # True if owner, False if just barber 
    profile_pic = models.ImageField(upload_to='images/', blank=True, null=True) # Can change file location and file type 
    phone_num = models.CharField(blank=True, null=True)                         # Barber personal phone number 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)            # Customers 
    Service = models.ForeignKey(Service, on_delete=models.CASCADE)              # Services 
    Review = models.ForeignKey(Review, on_delete=models.CASCADE)                # Reviews 

    # Functions to grab data, todo 
    def __str__(self):
        return self.barber_name


class Customer(models.Model):
    # In any of these fields, adjust max_length as needed 
    username = models.CharField(max_length=30, unique=True)                     # Needed when creating account 
    password = models.CharField(max_length=30, unique=True)                     # Needed when creating account 
    f_name = models.CharField(max_length=30, blank=True)                        # Set after account is created 
    l_name = models.CharField(max_length=30, blank=True)                        # Set after account is created 
    email = models.CharField(max_length=30, unique=True)                        # Needed when creating account 
    profile_pic = models.ImageField(upload_to='images/', blank=True, null=True) # Can change file location and file type 
    Review = models.ForeignKey(Review, on_delete=models.CASCADE)                # Reviews 
    
    # Functions to grab data, todo 
    def __str__(self):
        return f"{self.username}"


class Event(models.Model):
    date = models.DateField()                                                   # Needed when creating an Event 
    start_time = models.TimeField()                                             # Needed when creating an Event 
    end_time = models.TimeField()                                               # Needed when creating an Event 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)            # Customers 
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)                # Barbers 

    # Functions to grab data, todo 


class Service(models.Model):
    title = models.CharField()                                                  # Title of service, needed when creating Service 
    description = models.TextField(blank=True, null=True)                       # Description of service 
    price = models.FloatField()                                                 # Price of service, needed when creating Service
    duration = models.IntegerField()                                            # Duration of service, needed when creating Service 

    # Functions to grab data, todo 


class EventService(models.Model):
    # Events and services have a many to many relationship
    # Event can have multiple services (i.e. haircut, beard trim)
    # Service can have multiple events 
    event = models.ForeignKey(Event)                                            # Events
    service = models.ForeignKey(Service)                                        # Services 

    # Functions to grab data, todo 


class Review(models.Model):
    date = models.DateField(auto_now_add=True)                                  # Date of review, automatically sent to current date, needed when creating 
    rating = models.IntegerField()                                              # Rating of review, needed when creating 
    title = models.CharField(max_length=50)                                     # Title of review, needed when creating 
    description = models.TextField()                                            # Description of review, needed when creating 
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)            # Customer that set review 
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)                # Barber for review

    # Functions to grab data, todo 
    def __str__(self):
        return self.review_title


# Product, Blog Post, Gallery, Transaction will be added as needed 
