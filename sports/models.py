from turtle import title
from django.db import models
from courts.models import Court
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Sport(models.Model):
    name = models.CharField(max_length=100)
    courts = models.ManyToManyField(Court, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sports-detail', kwargs={'pk': self.pk})


class Slot(models.Model):
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, default='')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, default='')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'Slot:{self.id} on {self.date}'

    def get_absolute_url(self):
        return reverse('slots-detail', kwargs={'pk': self.pk})


class Booked_Slot(models.Model):
    slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
        return f'Booked Slots'


class FeaturedMatch(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main-home')
