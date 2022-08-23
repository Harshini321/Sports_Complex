from django.contrib import admin

# Register your models here.
from .models import Sport,Slot,Booked_Slot

admin.site.register(Sport)
admin.site.register(Slot)
admin.site.register(Booked_Slot)