from django.db import models
from django.conf import settings
from django.db.models import Q


class HoleCreater(models.Model):
    parkName = models.CharField(max_length=140)
    holeNumber = models.IntegerField()
    holeSub = models.CharField(max_length=1, blank=True, null=True)
    par = models.IntegerField()
    distance = models.IntegerField()
