from django.db import models
from django.contrib.auth.models import User
from sports.models import Slot
from courts.models import Court
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
        return self.user.username


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
        return self.user.username


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
        return self.user.username


RATE_CHOICES = [
    (1, '1 : Poor'),
    (2, '2 : Unsatisfactory'),
    (3, '3 : Satisfactory'),
    (4, '4 : Very Satisfactory'),
    (5, '5 : Outstanding')
]


class Rating(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f'Rating by {self.member.username} to {self.court.name}'

    def get_absolute_url(self):
        return reverse('courts-rating', kwargs={'pk': self.pk})
