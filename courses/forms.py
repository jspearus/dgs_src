from django import forms

from .models import HoleCreater


class HoleCreateForm(forms.Form):
    parkName = forms.CharField(max_length=140)
    holeNumber = forms.IntegerField()
    holeSub = forms.CharField(max_length=1, required=False)
    par = forms.IntegerField()
    distance = forms.IntegerField()


class HoleCreateModelForm(forms.ModelForm):
    class Meta:
        model = HoleCreater
        fields = ['parkName', 'holeNumber', 'holeSub', 'par', 'distance']
