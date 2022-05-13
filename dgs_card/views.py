from django.shortcuts import render
from django.template.loader import get_template


def home_page(request):
    title = "Welcome to DGScard"
    context = {"title": title}
    return render(request, "home.html", context)
