from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


from scorecards.models import ScoreCardCreator, ScoreCardHoleCreator
from accounts.models import ParkStats
from .models import GameCreator, CurrentGame, GameSave
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
    user = request.user
    gameOver = False
    title = name
    if park:
        new_game_creater(request, name)
        hole = CurrentGame.objects.filter(user=user, game=name).first()
        curHole = GameCreator.objects.filter(
            game=name, holeNumber=hole.cur_hole).first()
        print(f"hole: {hole.cur_hole}")
        print(f"throws: {curHole.throws}")
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        course = ScoreCardHoleCreator.objects.filter(
            card_name=name, holeNumber=hole.cur_hole).first()
        if 'Next' == request.POST.get('NavHole'):
            hole.cur_hole = hole.cur_hole + 1
            if hole.cur_hole > park.numOfHoles:
                hole.cur_hole = park.numOfHoles
            hole.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()
        elif 'Pre' == request.POST.get('NavHole'):
            hole.cur_hole = hole.cur_hole - 1
            if hole.cur_hole < 1:
                hole.cur_hole = 1
            hole.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()
        elif 'up' == request.POST.get('NavHole'):
            curHole.throws = curHole.throws + 1
            curHole.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()
        elif 'dn' == request.POST.get('NavHole'):
            curHole.throws = curHole.throws - 1
            if curHole.throws < 1:
                curHole.throws = 1
            curHole.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()
        elif 'UP' == request.POST.get('NavHole'):
            curHole.par = curHole.par + 1
            curHole.save()
            course.par = curHole.par
            course.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()
        elif 'DN' == request.POST.get('NavHole'):
            curHole.par = curHole.par - 1
            if curHole.par < 1:
                curHole.par = 1
            curHole.save()
            course.par = curHole.par
            course.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()

        elif 'save' == request.POST.get('NavHole'):
            holes = GameCreator.objects.filter(
                game=name, user=user)
            for h in holes:
                save = GameSave.objects.create(
                    user=user, card=name, hole=h.hole, holeNumber=h.holeNumber,
                    holeSub=h.holeSub, basket=h.basket, tee=h.tee,
                    distance=h.distance, par=h.par, throws=h.throws,
                    timestamp=h.timestamp)
            title = "Game Saved"

        if hole.cur_hole == park.numOfHoles:
            gameOver = True
    template_name = 'play_game/new-game.html'
    context = {'title': title, 'park': park.parkName,
               'hole': hole.cur_hole, 'par': curHole.par, 'throws': curHole.throws,
               'dist': curHole.distance, 'Score': curHole.throws - curHole.par,
               'CurScore': get_current_score(name), 'GameOver': gameOver}
    return render(request, template_name, context)


@login_required
def game_save_view(request, name):
    qs1 = []
    qs2 = []
    qs3 = []
    qs = GameSave.objects.filter(card=name)
    game = ScoreCardCreator.objects.filter(cardName=name).first()
    for q in qs:
        if q.holeNumber < 10:
            qs1.append(q)
        elif q.holeNumber < 19:
            qs2.append(q)
        else:
            qs3.append(q)
    context = {'course_list': qs1, 'course_list_2': qs2, 'course_list_3': qs3, 'name': name,
               'park': game.parkName, 'title': 'Saved Game Viewer'}
    template_name = 'play_game/game-save.html'
    return render(request, template_name, context)


def game_list_view(request):
    # list out / search for objects
    gList = []
    qs = GameSave.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.card not in gList:
                gList.append(q.card)
    template_name = 'home.html'
    context = {'games_list': gList}
    return render(request, template_name, context)


def get_current_score(name):
    holes = GameCreator.objects.filter(
        game=name)
    throws = 0
    par = 0
    for h in holes:
        throws = h.throws + throws
        par = h.par + par
        cScore = throws - par
    return cScore


def new_game_creater(request, card):
    qs = ScoreCardHoleCreator.objects.filter(card_name=card)
    print(f"card: {card}")
    hole = 1
    if request.user.is_authenticated:
        if not GameCreator.objects.filter(game=card):
            game_status = CurrentGame.objects.create(user=request.user,
                                                     game=card,
                                                     progress="started",
                                                     cur_hole=1)
            for q in qs:
                new_game = GameCreator.objects.create(user=request.user, game=card, hole=hole,
                                                      holeNumber=q.holeNumber, tee='white',
                                                      distance=q.distance, throws=q.par,
                                                      par=q.par)
                hole = hole+1
