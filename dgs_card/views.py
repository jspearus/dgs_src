from django.shortcuts import render
from django.template.loader import get_template

from .forms import ContactForm
from blog.models import BlogPost


def home_page(request):
    title = "Welcome to DGScard"
    context = {"title": title}
    return render(request, "home.html", context)
