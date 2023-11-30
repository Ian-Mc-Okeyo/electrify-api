from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=200, null=False, blank=False)
    lastName = models.CharField(max_length=200, null=False, blank=False)
    meterNumber = models.CharField(max_length=200, null=False, blank=False)
    phoneNumber = models.CharField(max_length=200, null=False, blank=False)

class UserData(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lastUpdate = models.DateTimeField(default=timezone.now)
    day = models.DateField()
    hour_1 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_2 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_3 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_4 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_5 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_6 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_7 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_8 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_9 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_10 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_11 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_12 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_13 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_14 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_15 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_16 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_17 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_18 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_19 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_20 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_21 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3) 
    hour_22 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_23 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
    hour_24 = models.DecimalField(max_digits=10, default=0.0, decimal_places=3)
       
