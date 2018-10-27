from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime


class Musician(models.Model):
    username = models.CharField(max_length=25)
    follower_count = models.IntegerField(default=0)
    balance = models.DecimalField(max_digits=11, decimal_places=2)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.id

class Authenticator(models.Model):
    user_id = models.CharField(max_length=25)
    authenticator = models.CharField(max_length=25, primary_key = True)
    date_created = models.DateField()


class SamplePack(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    purchase_count = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    num_samples = models.IntegerField(default=0)
    buyers = models.ManyToManyField(Musician, blank=True, related_name='buyers_set')
    current_seller = models.ForeignKey(Musician, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

class Sample(models.Model):
    name = models.CharField(max_length=50)
    minute_length = models.IntegerField(default=0)
    second_length = models.IntegerField(default=1)
    pack = models.ForeignKey(SamplePack, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


