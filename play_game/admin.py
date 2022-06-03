from django.contrib import admin


from .models import GameCreator, CurrentGame, GameSave
# Register your models here.
admin.site.register(GameCreator)
admin.site.register(CurrentGame)
admin.site.register(GameSave)
