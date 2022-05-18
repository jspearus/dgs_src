"""dgs_card URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import (
    home_page,
    sign_up_page,
    settings_page,
)
from courses.views import(
    course_list_view,
)
urlpatterns = [
    path('', course_list_view),
    # path('favicon.ico', RedirectView.as_view(
    #     url=staticfiles_storage.url('img/favicon.ico'))),
    path('admin/', admin.site.urls),
    path('', include("django.contrib.auth.urls")),  # new
    path('accounts/', include("accounts.urls")),
    path('', include("scorecards.urls")),
    path('', include("courses.urls")),
    path('settings/', settings_page),

]
