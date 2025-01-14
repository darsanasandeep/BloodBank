from logging import fatal
from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class BloodDonor(models.Model):
    fullname = models.CharField(max_length=100,null=False)
    age = models.IntegerField(null=False)
    email = models.EmailField(max_length=100,null=False)
    mobile_number = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=100, null=False)
    gender = models.CharField(max_length=100,null=False)
    health_issue = models.CharField(max_length=200,null=False)
    blood_type = models.CharField(max_length=100,null=False)
    status= models.CharField(max_length=100,null=False)

class BloodInventory(models.Model):
    blood_type = models.CharField(max_length=100, null=False)
    available_qnty = models.FloatField(null=False)


class BloodRequest(models.Model):
    request = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    age = models.IntegerField(null=True)
    mobile_number = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    blood_type = models.CharField(max_length=100, null=False)
    quantity = models.FloatField(null=False)
    status = models.CharField(max_length=100, null=False)


class DonationList(models.Model):
    donor = models.ForeignKey(BloodDonor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    blood_type = models.CharField(max_length=100, null=False)
    quantity = models.FloatField(null=False)
    status = models.BooleanField(default=False,null=False)




