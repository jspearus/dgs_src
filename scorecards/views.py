from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import ScoreCardCreator, ScoreCardHoleCreator
from courses.models import ParkCreator, HoleCreater
from .forms import ScoreCardCreatorModelForm
from courses.forms import ParkCreateModelForm, HoleCreateModelForm


@login_required
def create_scorecard_view(request):
    list = []
    title = ""
    qs = HoleCreater.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.parkName not in list:
                list.append(q.parkName)
        context = {'course_list': list}
    if request.method == 'POST':
        cardName = request.POST.get('cardName')
        parkName = request.POST.get('parkName')
        numOfHoles = request.POST.get('numOfHoles')
        form = ScoreCardCreatorModelForm(
            request.POST or None, request.FILES or None)
        title = "Error Creating Card"
        if form.is_valid():
            obj = form.save(commit=False)
            obj.cardName = cardName
            obj.parkName = parkName
            obj.numOfHoles = numOfHoles
            obj.save()
            form = ScoreCardCreatorModelForm()
            title = "Card Created"
        # print(f"{list}, {cardName}, {parkName}, {numOfHoles}")
        context = {'title': title, 'course_list': list}
        # new_card = ScoreCardCreator.objects.create(
        #     cardName=cardName,  parkName=parkName, numOfHoles=numOfHoles)
        # new_card.save()

    template_name = 'scorecards/newcardform.html'
    return render(request, template_name, context)

@login_required
def list_scorecards_view(request):
    list = []
    qs = ScoreCardCreator.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.cardName not in list:
                list.append(q.cardName)
        context = {'course_list': list}

    template_name = 'scorecards/card-list.html'
    return render(request, template_name, context)


@login_required
def edit_scorecard_view(request, cardName, holeNumber):
    courses = []
    qs = ParkCreator.objects.all().filter(cardName=cardName, holeNumber=holeNumber)
    for q in qs:
        if q.park_name not in courses:
            courses.append(q.park_name)
    print(courses)
    form = ScoreCardCreatorModelForm(
        request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = ScoreCardCreatorModelForm()
    template_name = 'scorecards/form.html'
    context = {'form': form, 'course_list': courses}
    if request.method == 'POST':
        # print(parkName)
        pass
    return render(request, template_name, context)
