from django import forms

from .models import HoleCreater


class HoleCreateForm(forms.Form):
    parkName = forms.CharField(max_length=140)
    holeNumber = forms.IntegerField()
    holeSub = forms.CharField(max_length=1, required=False)
    basket = forms.CharField(max_length=10)
    tee = forms.CharField(max_length=10)
    par = forms.IntegerField()
    distance = forms.IntegerField()


class HoleCreateModelForm(forms.ModelForm):
    class Meta:
        model = HoleCreater
        fields = ['parkName', 'holeNumber',
                  'basket', 'tee', 'holeSub', 'par', 'distance']
