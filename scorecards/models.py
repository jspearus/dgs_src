from django.db import models
from django.conf import settings
from django.db.models import Q

# Create your models here.


class ScoreCardCreator(models.Model):
    cardName = models.CharField(max_length=140)
    parkName = models.CharField(max_length=140)
    numOfHoles = models.IntegerField()
