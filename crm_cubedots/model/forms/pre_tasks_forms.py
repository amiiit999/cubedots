from django.forms import fields
from crm_cubedots.model.projects import Projects
from crm_cubedots.model.task import Tasks
from django import forms
from django.db import models
from crm_cubedots.model.pre_tasks import PreTasks

from crm_cubedots.model.departments import Departments
from crm_cubedots.model.task_categories import TaskCategories
from crm_cubedots.model.pre_tasks import PreTasks
from crm_cubedots.model.account import Account


#-------CONSTANTS-------
from crm_cubedots.constants.constants import TASK_PARENT_ID
from crm_cubedots.constants.constants import SELECT
from crm_cubedots.constants.constants import PARENT_ID


class PreTasksForm(forms.ModelForm):
    department = forms.ModelChoiceField(queryset=Departments.objects.filter(deleted_at = None), empty_label="Select")
    parent_id = forms.ChoiceField(choices=TASK_PARENT_ID,label="Parent Task") 
    def __init__(self, *args, **kwargs):
        super(PreTasksForm, self).__init__(*args, **kwargs)
        self.fields['parent_id'].choices = PARENT_ID + tuple(PreTasks.objects.filter(parent_id=0).values_list('id', 'taskid').order_by('taskid'))
        self.fields['task_category'].choices = SELECT + tuple(categories_as_choices())
    taskid        = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'TaskID'}))
    name          = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    description   = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,'style': 'height: 80px;','placeholder':'Description'}), required=False)
    required_time = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder':'Required Time (min)'}),label='Required time (min.)' )
    
    class Meta:
        model = PreTasks
        fields = ['name','department','parent_id','task_category','taskid','description','required_time']

def categories_as_choices():
    categories = []
    for category in TaskCategories.objects.only('id','name').filter(parent_id=0).order_by('name'):
        new_category = []
        sub_categories = []
        for sub_category in TaskCategories.objects.filter(parent_id = category.id):
            sub_categories.append([sub_category.id, sub_category.name])

        new_category = [category, sub_categories]
        categories.append(new_category)

    return categories      

class UploadPreTasksForm(forms.ModelForm):

    class Meta:
        model = PreTasks
        fields = ['name','department','parent_id','task_category','taskid','description','required_time']   

class ExportTasks(forms.ModelForm):
    project = forms.ModelChoiceField(queryset=Projects.objects.filter(deleted_at = None), empty_label="Select", label=False)

    class Meta:
        model = Tasks
        fields = ['project']
