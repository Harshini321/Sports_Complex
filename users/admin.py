from django.contrib import admin
from .models import Profile,Member,Admin,Staff,Rating
# Register your models here.
admin.site.register(Profile)
admin.site.register(Member)
admin.site.register(Admin)
admin.site.register(Staff)
admin.site.register(Rating)