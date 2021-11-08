from django import forms
from django.db import models
from crm_cubedots.model.project_categories import ProjectsCategories
from string import Template
from django.utils.safestring import mark_safe

class ProjectsCategoriesForm(forms.ModelForm):
    name = forms.CharField(label='Category Name',widget=forms.TextInput(attrs={'placeholder':'Enter Category Name'}))
    class Meta:
       model = ProjectsCategories
       fields = ['name']

       