from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import (
    create_hole_view,
    delete_hole_view,
)


urlpatterns = [
    path('create/', create_hole_view),
    path('deletecourse/', delete_hole_view),
]
