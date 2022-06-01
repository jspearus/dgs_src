from django.contrib import admin


from .models import GameCreator, CurrentGame
# Register your models here.
admin.site.register(GameCreator)
admin.site.register(CurrentGame)
