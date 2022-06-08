# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import ChangePasswordForm
from play_game.models import GameSave


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def edit_profile_page(request):
    user = request.user
    context = {"title": "test"}
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
    template_name = "accounts/editprofile.html"
    return render(request, template_name, context)


def Register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.info(
                request, "Thanks for registering. You are now logged in.")
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect("/")


@login_required
def save_game_stats(request):
    gList = []
    gObj = []
    cardName = ''
    qs = GameSave.objects.all()  # queryset -> list of python objects
    for q in qs:
        if q.card and (str(q.timestamp.day)+"d") and (str(q.timestamp.hour)+'h') and (str(q.timestamp.minute)+'m')not in gList:
            #  + str(q.timestamp.day) - used to get day of month from timestamp
            gList.append(q.card)
            gList.append(str(q.timestamp.day)+"d")
            gList.append(str(q.timestamp.hour)+'h')
            gList.append(str(q.timestamp.minute)+'m')
            gObj.append(q)
    context = {"title": "Player Stats", 'games_list': gObj}
    template_name = "accounts/user-stats.html"
    return render(request, template_name, context)
