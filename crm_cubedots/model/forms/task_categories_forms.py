from django import forms
from django.db import models
from itertools import chain

from crm_cubedots.model.task_categories import TaskCategories
from crm_cubedots.model.departments import Departments
from django.forms.fields import DateField, datetime
from crm_cubedots.constants.constants import PARENT_ID
    
"""    
class EmptyChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), empty_label=None, required=True, widget=None, label=None, initial=None, help_text=None, *args, **kwargs):

        # prepend an empty label if it exists (and field is not required!)
        if not required and empty_label is not None:
            choices = tuple([(u'0', empty_label)] + list(choices))

        super(EmptyChoiceField, self).__init__(choices=choices, required=required, widget=widget, label=label, initial=initial, help_text=help_text, *args, **kwargs) 

#parent_id = EmptyChoiceField(choices=TaskCategories.objects.filter(parent_id="0").values_list("id","name"), required=False, empty_label="Show All") 
"""

class TaskCategoriesForm(forms.ModelForm):
    name = forms.CharField(label='Task Category Name',widget=forms.TextInput(attrs={'placeholder':'Enter Task Category Name'}))
    department = forms.ModelChoiceField(queryset=Departments.objects.all(), empty_label="Select Department")
    #parent_id = forms.ChoiceField(choices=[[0, "Main Task"],["","Select"]] + [[r.id, r.name] for r in TaskCategories.objects.all()])
    parent_id = forms.ChoiceField(choices=PARENT_ID,label="Parent Category")
    def __init__(self, *args, **kwargs):
        super(TaskCategoriesForm, self).__init__(*args, **kwargs)
        self.fields['parent_id'].choices = PARENT_ID + tuple(TaskCategories.objects.filter(parent_id=0).values_list('id', 'name').order_by('name'))

    class Meta:
        model = TaskCategories
        fields = ['name','department','parent_id']