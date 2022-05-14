from django.shortcuts import render
from django.template.loader import get_template


def home_page(request):
    if request.method == "POST":
        title = "Submit Sucsessful"
    else:
        title = "Welcome to DGScard"
    context = {"title": title}
    return render(request, "home.html", context)


def sign_up_page(request):
    if request.method == "POST":
        title = "SIGNUP Sucsessful"
        context = {"title": title}
        return render(request, "home.html", context)
    title = "SIGNUP"
    context = {"title": title}
    return render(request, "signup.html", context)
