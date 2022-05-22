from django.contrib import admin

# Register your models here.
from .models import ParkCreator, HoleCreater

admin.site.register(ParkCreator)
admin.site.register(HoleCreater)
