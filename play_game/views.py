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
                    user=user, card=name, hole=h.hole, park=h.park,
                    holeNumber=h.holeNumber, holeSub=h.holeSub, basket=h.basket,
                    tee=h.tee, distance=h.distance, par=h.par, throws=h.throws,
                    timestamp=h.timestamp)
            curGame = CurrentGame.objects.filter(user=user)
            curGame.filter(user=user).delete()
            holes.delete()
            #  todo make this a function
            gList = []
            gObj = []
            gameStarted = 'false'
            qs = GameSave.objects.all()  # queryset -> list of python objects
            if request.user.is_authenticated:
                for q in qs:
                    if q.card and q.timestamp.day and q.timestamp.hour not in gList:
                        #  + str(q.timestamp.day) - used to get day of month from timestamp
                        gList.append(q.card)
                        gList.append(q.timestamp.day)
                        gList.append(q.timestamp.hour)
                        gObj.append(q)
            template_name = 'home.html'
            context = {'games_list': gObj, 'title': 'Game Saved',
                       'gameStarted': gameStarted}
            return render(request, template_name, context)

        elif 'del' == request.POST.get('NavHole'):
            holes = GameCreator.objects.filter(
                game=name, user=user)
            curGame = CurrentGame.objects.filter(user=user)
            curGame.filter(user=user).delete()
            holes.delete()
            #  todo make this a function
            gList = []
            gObj = []
            gameStarted = 'false'
            qs = GameSave.objects.all()  # queryset -> list of python objects
            if request.user.is_authenticated:
                for q in qs:
                    if q.card and q.timestamp.day and q.timestamp.hour not in gList:
                        #  + str(q.timestamp.day) - used to get day of month from timestamp
                        gList.append(q.card)
                        gList.append(q.timestamp.day)
                        gList.append(q.timestamp.hour)
                        gObj.append(q)
            template_name = 'home.html'
            context = {'games_list': gObj, 'title': 'Game Saved',
                       'gameStarted': gameStarted}
            return render(request, template_name, context)

        if hole.cur_hole == park.numOfHoles:
            gameOver = True
    template_name = 'play_game/new-game.html'
    context = {'title': title, 'park': park.parkName,
               'hole': hole.cur_hole, 'par': curHole.par, 'throws': curHole.throws,
               'dist': curHole.distance, 'Score': curHole.throws - curHole.par,
               'CurScore': get_current_score(name), 'GameOver': gameOver}
    return render(request, template_name, context)


@login_required
def game_save_view(request, name, day, hour):
    qs1 = []
    qs2 = []
    qs3 = []
    print(f"DAY: {day}")
    print(f"Hour: {hour}")
    qs = GameSave.objects.filter(card=name)
    game = GameSave.objects.filter(card=name).first()
    for q in qs:
        if str(q.timestamp.day) == day:
            game = q
    print(f"GameDay: {game.timestamp.day}")
    print(f"GameHour: {game.timestamp.hour}")
    for q in qs:
        if str(q.timestamp.day) == day and str(q.timestamp.hour) == hour:
            if q.holeNumber < 10:
                qs1.append(q)
            elif q.holeNumber < 19:
                qs2.append(q)
            else:
                qs3.append(q)
    tScore = get_final_score(name, day, hour)
    context = {'course_list': qs1, 'course_list_2': qs2, 'course_list_3': qs3,
               'park': game, 'tScore': tScore, 'title': "Saved Game"}
    template_name = 'play_game/game-save.html'
    return render(request, template_name, context)


def game_list_view(request):
    #  todo make this a function
    # list out / search for objects
    gList = []
    gObj = []
    cardName = ''
    gameStarted = 'false'
    if request.user.is_authenticated:
        if CurrentGame.objects.filter(user=request.user).exists():
            gameStarted = 'true'
        else:
            gameStarted = 'false'
    qs = GameSave.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            if q.card and q.timestamp.day and q.timestamp.hour not in gList:
                #  + str(q.timestamp.day) - used to get day of month from timestamp
                gList.append(q.card)
                cardName = q.card
                gList.append(q.timestamp.day)
                gList.append(q.timestamp.hour)
                gObj.append(q)
    template_name = 'home.html'
    context = {'games_list': gObj, 'cardName': cardName,
               'gameStarted': gameStarted}
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


def get_final_score(name, day, hour):
    holes = GameSave.objects.filter(
        card=name)
    throws = 0
    par = 0
    for h in holes:
        if str(h.timestamp.day) == day and str(h.timestamp.hour) == hour:
            throws = h.throws + throws
            par = h.par + par
            cScore = throws - par
    return cScore


def new_game_creater(request, card):
    qs = ScoreCardHoleCreator.objects.filter(card_name=card)
    print(f"card: {card}")
    hole = 1
    if request.user.is_authenticated:
        print(f"auth")
        if not GameCreator.objects.filter(game=card):
            print(f"gamestart")
            game_status = CurrentGame.objects.create(user=request.user,
                                                     game=card,
                                                     progress="started",
                                                     cur_hole=1)
            for q in qs:
                new_game = GameCreator.objects.create(user=request.user, game=card, park=q.park_name, hole=hole,
                                                      holeNumber=q.holeNumber, tee='white',
                                                      distance=q.distance, throws=q.par,
                                                      par=q.par)
                hole = hole+1
