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
            for x in range(int(numOfHoles)):
                qs = HoleCreater.objects.get(
                    parkName=parkName, holeNumber=x+1)

                record = ScoreCardHoleCreator.objects.create(
                    card_name=cardName, holeNumber=qs.holeNumber,
                    holeSub=qs.holeSub, basket=qs.basket, tee=qs.tee,
                    distance=qs.distance, par=qs.par
                )
            form = ScoreCardCreatorModelForm()
            title = "Card Created"
        context = {'title': title, 'course_list': list}
    template_name = 'scorecards/new-card.html'
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
def detail_scorecard_view(request, card):
    qs1 = []
    qs2 = []
    qs3 = []
    qs = ScoreCardHoleCreator.objects.filter(card_name=card)
    park = ScoreCardCreator.objects.filter(cardName=card).first()
    for q in qs:
        if q.holeNumber < 10:
            qs1.append(q)
        elif q.holeNumber < 19:
            qs2.append(q)
        else:
            qs3.append(q)
    context = {'course_list': qs1, 'course_list_2': qs2, 'course_list_3': qs3, 'name': card,
               'park': park.parkName, 'title': 'Hole Updated'}
    template_name = 'scorecards/card-detail.html'
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
