from django.db import models

class Barber(models.Model):
    barber_name = models.CharField(max_length=30, default="Default")
    reviews = models.IntegerField(default=0)
    def __str__(self):
        return self.barber_name

class Customer(models.Model):
    first_name = models.CharField(max_length=50, default="Firstname")
    last_name = models.CharField(max_length=50, default="Lastname")
    email = models.EmailField(unique=True, default="Email")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Review(models.Model):
    review_title = models.CharField(max_length=50, default="Default")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, null=True, default=None)
    rating = models.IntegerField(default=5)
    review_text = models.TextField()
    review_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.review_title
