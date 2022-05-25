from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import (
    create_scorecard_view,

)


urlpatterns = [
    path('cards/', create_scorecard_view),
]
