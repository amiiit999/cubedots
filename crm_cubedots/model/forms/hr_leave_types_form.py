from django import forms
from django.db import models

from crm_cubedots.model.leaves_type import LeaveTypes
from crm_cubedots.constants.constants import ACTIVE_STATUS

class LeaveTypesForm(forms.ModelForm):
    name = forms.CharField(label='Leave Name',widget=forms.TextInput(attrs={'placeholder':'Enter Leave Type Name'}))
    status = forms.ChoiceField(choices = ACTIVE_STATUS)
    class Meta:
       model = LeaveTypes
       fields = ['name','status']