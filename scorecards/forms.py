from django import forms

from .models import ScoreCardCreator, ScoreCardHoleCreator


class ScoreCardCreatorForm(forms.Form):
    cardName = forms.CharField(max_length=140)
    parkName = forms.CharField(max_length=140)
    numOfHoles = forms.IntegerField()


class ScoreCardHoleCreatorForm(forms.Form):
    card_name = forms.CharField(max_length=140, required=True)
    park_name = forms.CharField(max_length=140, required=True)
    hole = forms.IntegerField(required=True)
    holeNumber = forms.IntegerField()
    holeSub = forms.CharField(max_length=1, required=False)
    basket = forms.CharField(max_length=10)
    tee = forms.CharField(max_length=10)
    par = forms.IntegerField()
    distance = forms.IntegerField()


class ScoreCardCreatorModelForm(forms.ModelForm):

    class Meta:
        model = ScoreCardCreator
        fields = ['cardName', 'parkName', 'numOfHoles']


class ScoreCardHoleCreatorModelForm(forms.ModelForm):

    class Meta:
        model = ScoreCardHoleCreator
        fields = ['card_name', 'park_name', 'hole', 'holeNumber', 'holeSub', 'basket',
                  'tee', 'distance', 'par']
