from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.timezone import now
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

class UserComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    court=models.ForeignKey(Court,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return f'Court : {self.court.name}, Comment by { self.user.username }'
