from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import ScoreCardCreator, ScoreCardHoleCreator
from courses.models import ParkCreator, HoleCreater
from .forms import ScoreCardCreatorModelForm, ScoreCardHoleCreatorModelForm
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
                qs = HoleCreater.objects.filter(
                    parkName=parkName, holeNumber=x+1).first()
                record = ScoreCardHoleCreator.objects.create(
                    card_name=cardName, park_name=parkName, hole=x+1, holeNumber=qs.holeNumber,
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
    cardlist = []
    qs = ScoreCardCreator.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.cardName not in cardlist:
                cardlist.append(q.cardName)
        context = {'course_list': cardlist}

    template_name = 'scorecards/card-list.html'
    return render(request, template_name, context)


@login_required
def detail_scorecard_view(request, card):
    course_list = []
    qs = ScoreCardHoleCreator.objects.filter(card_name=card)
    park = ScoreCardCreator.objects.filter(cardName=card).first()
    for q in qs:
        course_list.append(q)
    context = {'course_list': course_list, 'name': card,
               'park': park.parkName, 'title': 'Hole Updated'}
    template_name = 'scorecards/card-detail.html'
    return render(request, template_name, context)


@login_required
def edit_scorecard_view(request, card, hole):
    # todo make custom form to edit scorecards..........
    if request.method == 'POST':
        if hole == 99:
            park = ScoreCardHoleCreator.objects.filter(
                card_name=card, hole=1).first()
            holeNum = ScoreCardCreator.objects.filter(
                parkName=park.park_name).first()
            hole = holeNum.numOfHoles+1

        if 'UpdateHole' == request.POST.get('NavHole'):
            newHole = request.POST.get('holeSelect')
            park = HoleCreater.objects.filter(id=newHole).first()
            print(f"newH: {park}")
            # todo needs to be in update if block below
            park.hole = request.POST.get('hole')
            park.card_name = card
            hole_list = HoleCreater.objects.filter(parkName=park.parkName)
            print(f"PArk: {park}")

        if 'update' == request.POST.get('NavHole'):
            newHole = request.POST.get('holeSelect')
            newH = HoleCreater.objects.filter(id=newHole).first()
            hole_list = HoleCreater.objects.filter(parkName=newH.parkName)
            print(f"newH: {newH}")
            # todo needs to be in update if block below
            park = ScoreCardHoleCreator.objects.filter(
                park_name=newH.parkName, hole=request.POST.get('hole')).update(
                    holeNumber=request.POST.get('holeNum'),
                    holeSub=request.POST.get('holeSub'),
                    basket=request.POST.get('basket'),
                    distance=request.POST.get('distance'),
                    tee=request.POST.get('tee'),
                    par=request.POST.get('par'))
            park = ScoreCardHoleCreator.objects.filter(
                park_name=newH.parkName, hole=request.POST.get('hole')).first()
            park.card_name = request.POST.get('card_name')

        title = 'Hole Updated!'
        template_name = 'scorecards/card-hole-edit.html'
        context = {'form': park, 'title': title, 'hole_list': hole_list}

        return render(request, template_name, context)

    if not hole == 99:
        park = ScoreCardHoleCreator.objects.filter(
            card_name=card, hole=hole).first()
        hole_list = HoleCreater.objects.filter(parkName=park.park_name)
        holeNum = ScoreCardCreator.objects.filter(
            parkName=park.park_name).first()
        addHole = park.hole

    else:
        park = ScoreCardHoleCreator.objects.filter(
            card_name=card, hole=1).first()
        holeNum = ScoreCardCreator.objects.filter(
            parkName=park.park_name).first()
        hole_list = HoleCreater.objects.filter(parkName=park.park_name)
        addHole = holeNum.numOfHoles+1
        print(f"Hole Numer: {addHole}")
        park.hole = addHole

    title = card
    template_name = 'scorecards/card-hole-edit.html'
    context = {'form': park, 'title': title, 'hole_list': hole_list}

    return render(request, template_name, context)
