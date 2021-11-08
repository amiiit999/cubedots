from django import forms
from django.db import models

from crm_cubedots.model.departments import Departments
from django.forms.fields import DateField, datetime
from crm_cubedots.constants.constants import ACTIVE_STATUS

class DepartmentsForm(forms.ModelForm):
    name = forms.CharField(label='Department Name',widget=forms.TextInput(attrs={'placeholder':'Enter Department Name'}))
    status = forms.ChoiceField(choices = ACTIVE_STATUS)
    class Meta:
       model = Departments
       fields = ['name','description','status']

class DepartmentSelectForm(forms.ModelForm):
    #card_choices = [(c.id, c.name) for c in Departments.objects.filter(deleted_at=None)]
    #department = forms.ChoiceField(required=True, widget=forms.Select(attrs={'onchange': 'actionform.submit();'}), choices=[(None, 'Select Type')]+card_choices)   
    department = forms.ModelChoiceField(queryset=Departments.objects.filter(deleted_at = None).order_by('name'),label=False,empty_label="Select Department", required=False, widget=forms.Select(attrs={"onChange":'this.form.submit()'}))
    class Meta:
        model = Departments
        fields = ['department']         