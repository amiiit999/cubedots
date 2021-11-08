from django import forms
from django.db import models
from crm_cubedots.model.project_categories import ProjectsCategories
from crm_cubedots.model.projects import Projects
from string import Template
from django.utils.safestring import mark_safe
from crm_cubedots.constants.constants import STATUS
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField, datetime


class ProjectsForm(forms.ModelForm):
    name = forms.CharField(label='Project Name',widget=forms.TextInput(attrs={'placeholder':'Enter Project Name'}))
    project_category = forms.ModelChoiceField(
        queryset=ProjectsCategories.objects.filter(deleted_at=None), 
        empty_label="Select Project Category")
    status = forms.ChoiceField(choices = STATUS)
    started_at = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta:
       model = Projects
       fields = ['name','description','status','project_category','started_at']

      