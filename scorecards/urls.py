from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import (
    create_scorecard_view,
    list_scorecards_view,
    edit_scorecard_view,
    detail_scorecard_view,

)


urlpatterns = [
    path('newcard/', create_scorecard_view),
    path('cards/', list_scorecards_view),
    path('card-edit/<str:card>/<int:hole>', edit_scorecard_view),
    path('card/<str:card>', detail_scorecard_view),
]
