# accounts/urls.py
from django.urls import path

from .views import (
    SignUpView,
    edit_profile_page
)


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('editprofile/', edit_profile_page),
]
