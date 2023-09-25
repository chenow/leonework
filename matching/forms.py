from django import forms
import environ
import os


from .models import *


class chatForms(forms.Form):
    job_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    student_id = forms.IntegerField(required=True, widget=forms.HiddenInput())
    chat = forms.CharField(required=True, max_length=2000)
    by = forms.CharField(required=True, max_length=20)
