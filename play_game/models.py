from django.db import models
from django.conf import settings
from django.db.models import Q


# Create your models here.
class GameCreator(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             default=1, null=True,
                             on_delete=models.SET_NULL)
    game = models.CharField(
        max_length=140, blank=False, null=False)
    hole = models.IntegerField(blank=False, null=False)
    holeNumber = models.IntegerField(blank=False, null=False)
    holeSub = models.CharField(max_length=1, blank=True)
    basket = models.CharField(max_length=10, blank=True)
    tee = models.CharField(max_length=10)
    distance = models.IntegerField(blank=False, null=False)
    throws = models.IntegerField(blank=False, null=False)
    par = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.game + str(self.hole)


class CurrentGame(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             default=1, null=True,
                             on_delete=models.SET_NULL)
    game = models.CharField(
        max_length=140, blank=False, null=False)
    progress = models.CharField(
        max_length=140, blank=False, null=False,
        default='Started')
    cur_hole = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.game + str(self.progress)
