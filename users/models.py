from django.db import models
from django.contrib.auth.models import User
from sports.models import Slot
from courts.models import Court
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


class Rating(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )

    def __str__(self):
        return f'Rating by {self.member.user.username} to {self.court.name}'
