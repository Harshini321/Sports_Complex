from django.db import models
from django.contrib.auth.models import User
from sports.models import Slot


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slots = models.ManyToManyField(Slot, blank=True)

    def __str__(self):
        return self.user.username
