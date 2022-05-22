from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
from .models import ParkCreator, HoleCreater
from .forms import ParkCreateModelForm, HoleCreateModelForm


def card_list_view(request):
    # list out / search for objects
    list = []
    qs = HoleCreater.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.parkName not in list:
                list.append(q.parkName)
    template_name = 'home.html'
    context = {'course_list': list}
    return render(request, template_name, context)


@login_required
def course_detail_view(request, name):
    # queryset -> list of python objects
    qs = HoleCreater.objects.filter(parkName__park_name=name)
    template_name = 'courses/park-detail.html'
    context = {'course_list': qs, 'name': name}
    return render(request, template_name, context)


@login_required
def course_list_view(request):
    # list out / search for objects
    list = []
    qs = HoleCreater.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.parkName not in list:
                list.append(q.parkName)
    template_name = 'courses/park-list.html'
    context = {'course_list': list}
    return render(request, template_name, context)


@login_required
def create_park_view(request):
    form = ParkCreateModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = ParkCreateModelForm()
    template_name = 'courses/parkform.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def create_hole_view(request):
    form = HoleCreateModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = HoleCreateModelForm()
    template_name = 'courses/form.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def delete_hole_view(request):
    template_name = 'courses/deletecourse.html'
    context = {'form': "none"}
    return render(request, template_name, context)
