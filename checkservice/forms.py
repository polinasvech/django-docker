from django import forms

class CheckForm(forms.Form):
    order = forms.CharField()