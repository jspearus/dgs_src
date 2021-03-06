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
    qs = HoleCreater.objects.filter(parkName=name)
    template_name = 'courses/park-detail.html'
    context = {'course_list': qs, 'name': name}
    return render(request, template_name, context)


@login_required
def hole_editor_view(request, name, hole):
    # queryset -> list of python objects
    qs = HoleCreater.objects.get(parkName=name, id=hole)
    form = HoleCreateModelForm(request.POST or None, instance=qs)
    form.fields['parkName'].widget.attrs['value'] = name
    form.fields['parkName'].widget.attrs['readonly'] = True
    if form.is_valid():
        form.save()
    template_name = 'courses/hole-edit.html'
    context = {'form': form, 'name': name}
    if request.method == "POST":
        qs = HoleCreater.objects.filter(parkName=name)
        template_name = 'courses/park-detail.html'
        context = {'course_list': qs, 'name': name, 'title': 'Hole Updated'}
        return render(request, template_name, context)
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
    title = ''
    if request.method == 'POST':
        form = ParkCreateModelForm(request.POST)
        name = form['park_name'].value()
        num = int(form['num_holes'].value())
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
        for x in range(num):
            record = HoleCreater.objects.create(
                parkName=name, holeNumber=x+1
            )
        title = "Park Created!"
    form = ParkCreateModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = ParkCreateModelForm()
    template_name = 'courses/parkform.html'
    context = {'form': form, 'title': title}
    return render(request, template_name, context)


@login_required
def create_hole_view(request, name):
    form = HoleCreateModelForm(
        request.POST or None, request.FILES or None)
    form.fields['parkName'].widget.attrs['value'] = name
    form.fields['parkName'].widget.attrs['readonly'] = True
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
    template_name = 'courses/form.html'
    context = {'form': form, 'name': name}
    if request.method == "POST":
        context = {'form': form, 'name': name, 'title': 'Hole Created!'}
    return render(request, template_name, context)


@login_required
def delete_hole_view(request):
    template_name = 'courses/deletecourse.html'
    context = {'form': "none"}
    return render(request, template_name, context)
