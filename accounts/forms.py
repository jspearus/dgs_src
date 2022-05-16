from django import forms


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField()
    confirm_password = forms.CharField()
