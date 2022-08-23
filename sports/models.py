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
    sport = models.ManyToManyField(Sport, blank=True)
    court = models.ManyToManyField(Court, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'Slot:{self.id} on {self.date}'

    def get_absolute_url(self):
        return reverse('slots-detail', kwargs={'pk': self.pk})


class Booked_Slot(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    booked_by=models.ForeignKey(User,on_delete=models.CASCADE,null=True)