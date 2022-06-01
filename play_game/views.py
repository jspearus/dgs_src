from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


from scorecards.models import ScoreCardCreator, ScoreCardHoleCreator
from .models import GameCreator
# Create your views here.


def new_game_select_view(request):
    cardlist = []
    qs = ScoreCardCreator.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.cardName not in cardlist:
                cardlist.append(q.cardName)
        context = {'card_list': cardlist}

    template_name = 'play_game/card-select.html'
    context = {'card_list': cardlist, 'title': "New Game"}
    return render(request, template_name, context)


def new_game_view(request, name):
    park = ScoreCardCreator.objects.filter(cardName=name).first()
    hole = 2
    cur_hole = ScoreCardHoleCreator.objects.filter(
        card_name=name, holeNumber=hole).first()
    score = 0
    cScore = -1
    user = None
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        if 'Next' == request.POST.get('NavHole'):
            hole = hole + 1
            cur_hole = ScoreCardHoleCreator.objects.filter(
                card_name=name, holeNumber=hole).first()
        elif 'Pre' == request.POST.get('NavHole'):
            hole = hole - 1
            cur_hole = ScoreCardHoleCreator.objects.filter(
                card_name=name, holeNumber=hole).first()
    template_name = 'play_game/new-game.html'
    context = {'title': name, 'park': park.parkName,
               'hole': hole, 'par': cur_hole.par, 'throws': cur_hole.par,
               'dist': cur_hole.distance, 'Score': score, 'CurScore': cScore,
               'GameOver': False}
    return render(request, template_name, context)
