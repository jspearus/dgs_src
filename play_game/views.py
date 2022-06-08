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
        course = ScoreCardHoleCreator.objects.filter(
            card_name=name, holeNumber=hole.cur_hole).first()
        park_stat = get_park_stats(user, course, hole.cur_hole)

        print(f"basket: {course.holeSub}")
        print(f"holesub: {course.tee}")
        print(f"curHole: {curHole}")
    if request.user.is_authenticated:
        user = request.user
    if request.method == 'POST':
        course = ScoreCardHoleCreator.objects.filter(
            card_name=name, holeNumber=hole.cur_hole).first()
        park_stat = get_park_stats(user, course, hole.cur_hole)

        if 'Next' == request.POST.get('NavHole'):
            hole.cur_hole = hole.cur_hole + 1
            if hole.cur_hole > park.numOfHoles:
                hole.cur_hole = park.numOfHoles
            hole.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()
            park_stat = get_park_stats(user, course, hole.cur_hole)

        elif 'Pre' == request.POST.get('NavHole'):
            hole.cur_hole = hole.cur_hole - 1
            if hole.cur_hole < 1:
                hole.cur_hole = 1
            hole.save()
            curHole = GameCreator.objects.filter(
                game=name, holeNumber=hole.cur_hole).first()
            park_stat = get_park_stats(user, course, hole.cur_hole)

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
                if ParkStats.objects.filter(
                        user=user, park=h.park, holeNumber=h.holeNumber,
                        holeSub=h.holeSub, basket=h.basket, tee=h.tee).exists():
                    hole = ParkStats.objects.filter(
                        user=user, park=h.park, holeNumber=h.holeNumber,
                        holeSub=h.holeSub, basket=h.basket, tee=h.tee).first()
                    ParkStats.objects.filter(
                        user=user, park=h.park, holeNumber=h.holeNumber,
                        holeSub=h.holeSub, basket=h.basket, tee=h.tee).update(
                            throws=hole.throws+h.throws, timesPlayed=hole.timesPlayed+1)
                else:
                    ParkStats.objects.create(
                        user=user, park=h.park, holeNumber=h.holeNumber,
                        holeSub=h.holeSub,
                        basket=h.basket, tee=h.tee, throws=h.throws,
                        timesPlayed=1)
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
                    if q.card and (str(q.timestamp.day)+"d") and (str(q.timestamp.hour)+'h') not in gList:
                        #  + str(q.timestamp.day) - used to get day of month from timestamp
                        gList.append(q.card)
                        gList.append(str(q.timestamp.day)+"d")
                        gList.append(str(q.timestamp.hour)+'h')
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
                    if q.card and (str(q.timestamp.day)+"d") and (str(q.timestamp.hour)+'h') not in gList:
                        #  + str(q.timestamp.day) - used to get day of month from timestamp
                        gList.append(q.card)
                        gList.append(str(q.timestamp.day)+"d")
                        gList.append(str(q.timestamp.hour)+'h')
                        gObj.append(q)
            template_name = 'home.html'
            context = {'games_list': gObj, 'title': 'Game Saved',
                       'gameStarted': gameStarted}
            return render(request, template_name, context)

        if hole.cur_hole == park.numOfHoles:
            gameOver = True
    template_name = 'play_game/new-game.html'
    context = {'title': title, 'park': park.parkName,
               'hole': hole.cur_hole, 'par': curHole.par,
               'avg': round(park_stat.throws/park_stat.timesPlayed, 1),
               'throws': curHole.throws,
               'dist': curHole.distance, 'Score': curHole.throws - curHole.par,
               'CurScore': get_current_score(name), 'GameOver': gameOver}
    return render(request, template_name, context)


def get_park_stats(user, course, curHole):
    park_stat = ParkStats.objects.filter(
        user=user, park=course.park_name,
        holeNumber=curHole,
        holeSub=course.holeSub,
        basket=course.basket,
        tee=course.tee).first()
    if park_stat.throws == 0 and park_stat.timesPlayed == 0:
        park_stat.throws = 99
        park_stat.timesPlayed = 1
    return park_stat


@login_required
def game_save_view(request, name, day, hour):
    qs1 = []
    qs2 = []
    qs3 = []
    qs = GameSave.objects.filter(card=name)
    game = GameSave.objects.filter(card=name).first()
    for q in qs:
        if str(q.timestamp.day) == day:
            game = q
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
            game = CurrentGame.objects.filter(user=request.user).first()
            cardName = game.game
        else:
            gameStarted = 'false'
    qs = GameSave.objects.all()  # queryset -> list of python objects
    if request.user.is_authenticated:
        for q in qs:
            # todo for debug
            print(f"DAY: {q.timestamp.day}")
            print(f"Hour: {q.timestamp.hour}")
            print(f"list: {gList}")
            print(f"obj: {gObj}")
        # todo for debug
            if q.card and (str(q.timestamp.day)+"d") and (str(q.timestamp.hour)+'h') not in gList:
                #  + str(q.timestamp.day) - used to get day of month from timestamp
                gList.append(q.card)
                gList.append(str(q.timestamp.day)+"d")
                gList.append(str(q.timestamp.hour)+'h')
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
    user = request.user
    if request.user.is_authenticated:
        print(f"auth")
        if not GameCreator.objects.filter(game=card):
            print(f"gamestart")
            game_status = CurrentGame.objects.create(user=user,
                                                     game=card,
                                                     progress="started",
                                                     cur_hole=1)
            for q in qs:
                new_game = GameCreator.objects.create(user=user, game=card, park=q.park_name, hole=hole,
                                                      holeNumber=q.holeNumber, holeSub=q.holeSub, basket=q.basket,
                                                      tee=q.tee,
                                                      distance=q.distance, throws=q.par,
                                                      par=q.par)
                hole = hole+1
                if not ParkStats.objects.filter(
                        user=user, park=q.park_name,
                        holeNumber=q.holeNumber, holeSub=q.holeSub, basket=q.basket,
                        tee=q.tee).exists():
                    ParkStats.objects.create(
                        user=user, park=q.park_name, holeNumber=q.holeNumber,
                        holeSub=q.holeSub,
                        basket=q.basket, tee=q.tee, throws=0,
                        timesPlayed=0)
