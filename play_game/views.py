from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


from scorecards.models import ScoreCardCreator, ScoreCardHoleCreator
from courses.models import HoleCreater
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
    parkName = ScoreCardCreator.objects.filter(cardName=name).first()
    user = request.user
    gameOver = False
    title = name
    if parkName:
        if not CurrentGame.objects.all():
            new_game_creater(request, name)
        hole_list = HoleCreater.objects.filter(parkName=parkName.parkName)
        hole = CurrentGame.objects.filter(user=user).first()
        curHole = GameCreator.objects.filter(
            hole=hole.cur_hole).first()
        course = ScoreCardHoleCreator.objects.filter(
            card_name=name, holeNumber=hole.cur_hole).first()
        park_stat = get_park_stats(user, course, hole.cur_hole)
        # todo for debug
        # print(f"basket: {course.holeSub}")
        # print(f"holesub: {course.tee}")
        # print(f"curHole: {curHole}")
        # todo for debug
    if request.method == 'POST':
        print(f"hole Id: {request.POST.get('holeSelect')}")
        print(f"Btn Id: {request.POST.get('NavHole')}")
        course = ScoreCardHoleCreator.objects.filter(
            card_name=name, holeNumber=hole.cur_hole).first()
        park_stat = get_park_stats(user, course, hole.cur_hole)

        if 'Next' == request.POST.get('NavHole'):
            hole.cur_hole = hole.cur_hole + 1
            if hole.cur_hole > parkName.numOfHoles:
                hole.cur_hole = parkName.numOfHoles
            hole.save()
            curHole = GameCreator.objects.filter(
                game=name, hole=hole.cur_hole).first()
            park_stat = get_park_stats(user, course, hole.cur_hole)

        elif 'Pre' == request.POST.get('NavHole'):
            hole.cur_hole = hole.cur_hole - 1
            if hole.cur_hole < 1:
                hole.cur_hole = 1
            hole.save()
            curHole = GameCreator.objects.filter(
                game=name, hole=hole.cur_hole).first()
            park_stat = get_park_stats(user, course, hole.cur_hole)

        elif 'up' == request.POST.get('NavHole'):
            curHole.throws = curHole.throws + 1
            curHole.save()
            curHole = GameCreator.objects.filter(
                game=name, hole=hole.cur_hole).first()
        elif 'dn' == request.POST.get('NavHole'):
            curHole.throws = curHole.throws - 1
            if curHole.throws < 1:
                curHole.throws = 1
            curHole.save()
            curHole = GameCreator.objects.filter(
                game=name, hole=hole.cur_hole).first()
        elif 'UP' == request.POST.get('NavHole'):
            curHole.par = curHole.par + 1
            curHole.save()
            course.par = curHole.par
            course.save()
            curHole = GameCreator.objects.filter(
                game=name, hole=hole.cur_hole).first()
        elif 'DN' == request.POST.get('NavHole'):
            curHole.par = curHole.par - 1
            if curHole.par < 1:
                curHole.par = 1
            curHole.save()
            course.par = curHole.par
            course.save()
            curHole = GameCreator.objects.filter(
                game=name, hole=hole.cur_hole).first()

        elif 'Update' == request.POST.get('NavHole'):
            holeId = request.POST.get('holeSelect')
            curHole = GameCreator.objects.filter(
                game=name, hole=hole.cur_hole).first()
            update_game_view(request, curHole.game, curHole.hole,  holeId)

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
            if request.user.is_authenticated:
                qs = GameSave.objects.filter(
                    user=request.user).order_by('-timestamp')
                for q in qs:
                    # todo for debug
                    # print(f"DAY: {q.timestamp.day}")
                    # print(f"Hour: {q.timestamp.hour}")
                    # print(f"min: {q.timestamp.minute}")
                    # print(f"list: {gList}")
                    # print(f"obj: {gObj}")
                    # todo for debug
                    if q.card and (str(q.timestamp.day)+"d") and (str(q.timestamp.hour)+'h') and (str(q.timestamp.minute)+'m')not in gList:
                        #  + str(q.timestamp.day) - used to get day of month from timestamp
                        gList.append(q.card)
                        gList.append(str(q.timestamp.day)+"d")
                        gList.append(str(q.timestamp.hour)+'h')
                        gList.append(str(q.timestamp.minute)+'m')
                        if len(gObj) < 3:
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
            if request.user.is_authenticated:
                qs = GameSave.objects.filter(
                    user=request.user).order_by('-timestamp')
                for q in qs:
                    # todo for debug
                    # print(f"DAY: {q.timestamp.day}")
                    # print(f"Hour: {q.timestamp.hour}")
                    # print(f"min: {q.timestamp.minute}")
                    # print(f"list: {gList}")
                    # print(f"obj: {gObj}")
                    # todo for debug
                    if q.card and (str(q.timestamp.day)+"d") and (str(q.timestamp.hour)+'h') and (str(q.timestamp.minute)+'m')not in gList:
                        #  + str(q.timestamp.day) - used to get day of month from timestamp
                        gList.append(q.card)
                        gList.append(str(q.timestamp.day)+"d")
                        gList.append(str(q.timestamp.hour)+'h')
                        gList.append(str(q.timestamp.minute)+'m')
                        if len(gObj) < 3:
                            gObj.append(q)
            template_name = 'home.html'
            context = {'games_list': gObj, 'title': 'Game Saved',
                       'gameStarted': gameStarted}
            return render(request, template_name, context)

        if hole.cur_hole == parkName.numOfHoles:
            gameOver = True
    hole = CurrentGame.objects.filter(user=user).first()
    curHole = GameCreator.objects.filter(
        game=name, hole=hole.cur_hole).first()
    template_name = 'play_game/new-game.html'
    context = {'title': title, 'park': parkName.parkName,
               'hole_list': hole_list,
               'hole': curHole,
               'avg': round(park_stat.throws/park_stat.timesPlayed, 1),
               'throws': curHole.throws, 'dist': curHole.distance, 'Score': curHole.throws - curHole.par,
               'CurScore': get_current_score(name), 'GameOver': gameOver}
    return render(request, template_name, context)

# todo Fix This.....


@login_required
def update_game_view(request, game, gHole,  hole):
    print(f"game: {game}")
    print(f"gHole: {gHole}")
    print(f"hole: {hole}")
    user = request.user
    new_hole = HoleCreater.objects.filter(id=hole).first()
    curGamehole = CurrentGame.objects.filter(user=user, game=game).first()
    curHole = GameCreator.objects.filter(
        game=game, hole=gHole).first()
    course = ScoreCardHoleCreator.objects.filter(
        card_name=game, holeNumber=curGamehole.cur_hole).first()
    park_stat = get_park_stats(user, course, curGamehole.cur_hole)
    hole_list = HoleCreater.objects.filter(parkName=curHole.park)
    user = request.user
    gameOver = False
    newHole = GameCreator.objects.filter(
        user=user,  hole=curHole.hole).first()
    print(f"new tee: {new_hole.tee}")
    GameCreator.objects.filter(user=user,  hole=curHole.hole).update(
        holeNumber=new_hole.holeNumber, holeSub=new_hole.holeSub,
        basket=new_hole.basket, tee=new_hole.tee, distance=new_hole.distance,
        throws=new_hole.par, par=new_hole.par)
    print(f"Saved tee: {newHole.tee}")


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
def game_save_view(request, name, day, hour, Minute):
    qs1 = []
    qs2 = []
    qs3 = []
    qs = GameSave.objects.filter(user=request.user, card=name)
    game = GameSave.objects.filter(user=request.user, card=name).first()
    #  remove leading zero from single digit minute
    if int(Minute) < 10:
        new_minute = list(Minute)
        Minute = new_minute[1]
    for q in qs:
        if str(q.timestamp.day) == day and str(q.timestamp.hour) == hour and str(q.timestamp.minute) == Minute:
            game = q
    for q in qs:
        if str(q.timestamp.day) == day and str(q.timestamp.hour) == hour and str(q.timestamp.minute) == Minute:
            if q.holeNumber < 10:
                qs1.append(q)
            elif q.holeNumber < 19:
                qs2.append(q)
            else:
                qs3.append(q)
    tScore = get_final_score(name, day, hour, Minute)
    context = {'course_list': qs1, 'course_list_2': qs2, 'course_list_3': qs3,
               'park': game, 'tScore': tScore, 'title': "Saved Game"}
    template_name = 'play_game/game-save.html'
    return render(request, template_name, context)


def park_stat_view(request, park):
    qs1 = []
    qs2 = []
    qs3 = []
    qs = ParkStats.objects.filter(user=request.user, park=park)
    park = ParkStats.objects.filter(user=request.user, park=park).first()
    for q in qs:
        if q.holeNumber < 10:
            qs1.append(q)
        elif q.holeNumber < 19:
            qs2.append(q)
        else:
            qs3.append(q)
    context = {'park_list': qs1, 'park_list_2': qs2, 'park_list_3': qs3,
               'park': park, 'title': "Park Stats"}
    template_name = 'accounts/park-stats.html'
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
    # queryset -> list of python objects
    if request.user.is_authenticated:
        qs = GameSave.objects.filter(user=request.user).order_by('-timestamp')
        for q in qs:
            # todo for debug
            # print(f"DAY: {q.timestamp.day}")
            # print(f"Hour: {q.timestamp.hour}")
            # print(f"min: {q.timestamp.minute}")
            # print(f"list: {gList}")
            # print(f"obj: {gObj}")
            # todo for debug
            if q.card and (str(q.timestamp.day)+"d") and (str(q.timestamp.hour)+'h') and (str(q.timestamp.minute)+'m')not in gList:
                #  + str(q.timestamp.day) - used to get day of month from timestamp
                gList.append(q.card)
                gList.append(str(q.timestamp.day)+"d")
                gList.append(str(q.timestamp.hour)+'h')
                gList.append(str(q.timestamp.minute)+'m')
                if len(gObj) < 3:
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


def get_final_score(name, day, hour, minute):
    holes = GameSave.objects.filter(
        card=name)
    throws = 0
    par = 0
    for h in holes:
        if str(h.timestamp.day) == day and str(h.timestamp.hour) == hour and str(h.timestamp.minute) == minute:
            throws = h.throws + throws
            par = h.par + par
            cScore = throws - par
    return cScore


def new_game_creater(request, card):
    qs = ScoreCardHoleCreator.objects.filter(card_name=card)
    hole = 1
    user = request.user
    if request.user.is_authenticated:
        if not GameCreator.objects.filter(game=card):
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
