from django.contrib import admin

# Register your models here.
from .models import ScoreCardCreator, ScoreCardHoleCreator

admin.site.register(ScoreCardCreator)
admin.site.register(ScoreCardHoleCreator)
