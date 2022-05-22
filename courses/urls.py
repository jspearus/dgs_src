from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import (
    create_park_view,
    course_detail_view,
    create_hole_view,
    delete_hole_view,
    card_list_view,

)


urlpatterns = [
    path('create/', create_hole_view),
    path('newpark/', create_park_view),
    path('deletecourse/', delete_hole_view),
    path('park/', card_list_view),
    path('park-detail/<str:name>', course_detail_view),
]
