# accounts/urls.py
from django.urls import path

from .views import (
    SignUpView,
    edit_profile_page,
    save_game_stats
)


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    #  path("registration/signup/", Register, name="signup"),
    path('editprofile/', edit_profile_page),
    path('userstats/', save_game_stats),
]
