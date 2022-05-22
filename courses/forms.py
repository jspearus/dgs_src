from django import forms

from .models import ParkCreator, HoleCreater


class ParkCreateForm(forms.Form):
    park_name = forms.CharField(max_length=140)
    num_holes = forms.IntegerField()


class HoleCreateForm(forms.Form):
    parkName = forms.CharField(max_length=140)
    holeNumber = forms.IntegerField()
    holeSub = forms.CharField(max_length=1, required=False)
    basket = forms.CharField(max_length=10)
    tee = forms.CharField(max_length=10)
    par = forms.IntegerField()
    distance = forms.IntegerField()


class ParkCreateModelForm(forms.ModelForm):
    class Meta:
        model = ParkCreator
        fields = ['park_name', 'num_holes']


class HoleCreateModelForm(forms.ModelForm):
    class Meta:
        model = HoleCreater
        fields = ['parkName', 'holeNumber',
                  'basket', 'tee', 'holeSub', 'distance', 'par']
