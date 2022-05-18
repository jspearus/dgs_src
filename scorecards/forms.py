from django import forms

from .models import ScoreCardCreator


class ScoreCardCreatorForm(forms.Form):
    cardName = forms.CharField(max_length=140)
    parkName = forms.CharField(max_length=140)
    numOfHoles = forms.IntegerField()


class ScoreCardCreatorModelForm(forms.ModelForm):

    class Meta:
        model = ScoreCardCreator
        fields = ['cardName', 'parkName', 'numOfHoles']
