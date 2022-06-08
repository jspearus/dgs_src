from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import (
    new_game_select_view,
    new_game_view,
    game_save_view,
    park_stat_view
)

urlpatterns = [
    path('newgame/', new_game_select_view),
    path('new-game/<str:name>', new_game_view),
    path('save-game/<str:name>/<str:day>/<str:hour>/<str:Minute>', game_save_view),
    path('park-stats/<str:park>', park_stat_view),
]
