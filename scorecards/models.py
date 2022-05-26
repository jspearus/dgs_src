from django.db import models
from django.conf import settings
from django.db.models import Q


# Create your models here.
from courses.models import ParkCreator


class ScoreCardCreator(models.Model):
    cardName = models.CharField(
        max_length=140, unique=True, blank=False, null=False)
    parkName = models.CharField(max_length=140)
    numOfHoles = models.IntegerField(blank=False, null=False)
    # used to declare what is shown in form dropdown menus

    def __str__(self):
        return self.cardName
    
class ScoreCardHoleCreator(models.Model):
    card_name = models.CharField(
        max_length=140, unique=True, blank=False, null=False)
    holeNumber = models.IntegerField(blank=False, null=False)
    holeSub = models.CharField(max_length=1, blank=True)
    basket = models.CharField(max_length=10, blank=True)
    tee = models.CharField(max_length=10, default='White')
    distance = models.IntegerField(blank=False, null=False)
    par = models.IntegerField(blank=False, null=False)