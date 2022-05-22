from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.


class ScoreCardCreator(models.Model):
    cardName = models.CharField(max_length=140)
    parkName = models.CharField(max_length=140)
    numOfHoles = models.IntegerField()
    # used to declare what is shown in form dropdown menus

    def __str__(self):
        return self.cardName
