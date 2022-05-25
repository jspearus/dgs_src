from django.db import models
from django.conf import settings
from django.db.models import Q


class CourseQuerySet(models.QuerySet):
    def published(self):
        return self.all()


class CourseManager(models.Manager):
    def get_courses(self):
        return CourseQuerySet(self.model, using=self._db)


class ParkCreator(models.Model):
    park_name = models.CharField(
        max_length=140, unique=True, blank=False, null=False)
    num_holes = models.IntegerField()

    # used to declare what is shown in form dropdown menus
    def __str__(self):
        return self.park_name


class HoleCreater(models.Model):
    parkName = models.CharField(
        max_length=140, blank=False, null=False)
    holeNumber = models.IntegerField()
    holeSub = models.CharField(max_length=1, blank=True)
    basket = models.CharField(max_length=10, blank=True)
    tee = models.CharField(max_length=10, default='White')
    par = models.IntegerField(default=3)
    distance = models.IntegerField(default=250)

    def __str__(self):
        return self.parkName + str(self.holeNumber)
