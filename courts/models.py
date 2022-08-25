from django.db import models
from django.urls import reverse
# from users.models import Member
# from sports.models import Slot

# Create your models here.
class Court(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courts-detail', kwargs={'pk': self.pk})


