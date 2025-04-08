from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User_details(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=10,unique=True)
    gender=models.CharField(max_length=100)
    address=models.TextField()

class Halls(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=200)
    capacity=models.IntegerField()
    price_per_day=models.DecimalField(max_digits=10,decimal_places=2)
    photo_url=models.ImageField(upload_to='images/')
    description=models.TextField(blank=True,null=True)

class Food(models.Model):
    food_name=models.CharField(max_length=100,null=True)
    food_image=models.ImageField(upload_to='images/')
    food_price=models.DecimalField(max_digits=10,decimal_places=2)

class Decoration(models.Model):
    decoration_name=models.CharField(max_length=100,null=True)
    decoration_image=models.ImageField(upload_to='images/')
    decoration_price=(models.DecimalField(max_digits=10,decimal_places=2))   

class Bookings(models.Model):
    event_date=models.DateField(null=True)
    event_status=models.CharField(max_length=100,default='Pending')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    hall_id=models.ForeignKey(Halls,on_delete=models.CASCADE)
    booking_date=models.DateField(auto_now_add=True)
    payment_status=models.CharField(max_length=100,default='Pending')
    photography=models.CharField(max_length=100,null=True,blank=True)
    no_of_persons=models.IntegerField(null=True,blank=True)
    food_value=models.BooleanField(null=True,blank=True)
    food=models.ForeignKey(Food,on_delete=models.SET_NULL, null=True, blank=True)
    decoration_value=models.BooleanField(null=True,blank=True)
    decoration=models.ForeignKey(Decoration,on_delete=models.SET_NULL, null=True, blank=True)
    photography_cost=models.DecimalField(max_digits=10,decimal_places=2)
    total_payment=models.DecimalField(max_digits=10,decimal_places=2)

