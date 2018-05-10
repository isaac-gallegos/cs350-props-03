# forms.py

from django import forms
from django.forms import Form

class LookupForm(Form):
    search = forms.CharField(widget=forms.TextInput)

class DistanceForm(Form):
    location = forms.CharField(widget=forms.TextInput)
    miles = forms.IntegerField(widget=forms.TextInput)