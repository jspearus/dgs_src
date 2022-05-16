# accounts/urls.py
from django.urls import path

from .views import SignUpView, Register



urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    #  path("registration/signup/", Register, name="signup"),
]
