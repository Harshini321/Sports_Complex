from django.contrib import admin

# Register your models here.
from .models import Court, UserComment

admin.site.register(Court)
admin.site.register(UserComment)