from django.db import models
from django.conf import settings
from django.db.models import Q


class CourseQuerySet(models.QuerySet):
    def published(self):
        return self.all()


class CourseManager(models.Manager):
    def get_courses(self):
        return CourseQuerySet(self.model, using=self._db)


class HoleCreater(models.Model):
    parkName = models.CharField(max_length=140)
    holeNumber = models.IntegerField()
    holeSub = models.CharField(max_length=1, default='A')
    basket = models.CharField(max_length=10, default='A')
    tee = models.CharField(max_length=10, default='Red')
    par = models.IntegerField()
    distance = models.IntegerField()
