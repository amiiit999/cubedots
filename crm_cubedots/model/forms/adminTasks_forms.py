from crm_cubedots.model.pre_tasks import PreTasks
from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from crm_cubedots.model.task import Tasks
from django.forms.fields import DateField, datetime
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


from crm_cubedots.model.task import Tasks
from crm_cubedots.model.account import Account
from crm_cubedots.model.departments import Departments
from crm_cubedots.model.task_categories import TaskCategories

#-------CONSTANTS-------
from crm_cubedots.constants.constants import TASK_PARENT_ID
from crm_cubedots.constants.constants import YES_NO
from crm_cubedots.constants.constants import TASK_STATUS
from crm_cubedots.constants.constants import TASK_PROCESS_STATUS
from crm_cubedots.constants.constants import SELECT
from crm_cubedots.model.projects import Projects
from crm_cubedots.constants.constants import PRIORITY

from django.db.models import Q

from django.db.models import query

class AdminTasksForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Account.objects.filter(deleted_at=None), empty_label="Select", label="User")
    department = forms.ModelChoiceField(queryset=Departments.objects.filter(deleted_at=None) , empty_label="Select")
    tl = forms.ModelChoiceField(queryset=Account.objects.filter(role__in=['tl']).order_by('first_name'), empty_label="Select")
    qc = forms.ModelChoiceField(queryset=Account.objects.filter(role__in=['qa','tl']).order_by('first_name'), empty_label="Select")
    parent_id = forms.ChoiceField(choices=TASK_PARENT_ID,label="Parent Task") 
    def __init__(self, *args, **kwargs):
        self.parent_id_arg = kwargs.pop('parent_id_arg')
        super(AdminTasksForm, self).__init__(*args, **kwargs)
        
        self.fields['parent_id'].choices = TASK_PARENT_ID + tuple(Tasks.objects.filter(parent_id=0, project_id = self.parent_id_arg, deleted_at=None).values_list('id', 'taskid').order_by('name'))
        
        self.fields['task_category'].choices = SELECT + tuple(categories_as_choices())
    #task_category = forms.ModelChoiceField(queryset=TaskCategories.objects.all(), empty_label="Select")
    #print (Tasks.objects.filter(parent_id=0,project_id = self.instance.id).values_list('id', 'taskid').order_by('name'))
    dependency_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Dependency id'}))
    is_extra      = forms.ChoiceField(choices=YES_NO, label="Is Extra Task? ")
    taskid        = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'TaskID'}))
    name          = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Name'}))
    description   = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,'style': 'height: 80px;','placeholder':'Description'}))
    status        = forms.ChoiceField(choices=TASK_STATUS, label="Task Status")
    process_status= forms.ChoiceField(choices=TASK_PROCESS_STATUS, label="Task Process Status")
    task_started_at = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    task_ended_at = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    task_duration   = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Task Duration'}))
    priority      = forms.ChoiceField(choices=PRIORITY,label="Task Priority")  
    class Meta:
            model = Tasks
            fields = ['priority','department', 'dependency_id', 'description', 'is_extra', 'name', 'parent_id', 'process_status', 'status', 'task_category', 'task_duration', 'task_ended_at', 'task_started_at', 'taskid', 'tl', 'user','qc']
    
    

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
       
class PreTasksCreateBulkForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Account.objects.all(), empty_label="Select", label=False)
    tl = forms.ModelChoiceField(queryset=Account.objects.filter(role__in=['tl']).order_by('first_name'), empty_label="Select", label=False)
    qc = forms.ModelChoiceField(queryset=Account.objects.filter(role__in=['qa','tl']).order_by('first_name'), empty_label="Select", label=False)
    
    task_category_id = forms.ChoiceField(label=False)
    def __init__(self, *args, **kwargs):
        
        super(PreTasksCreateBulkForm, self).__init__(*args, **kwargs)
        self.fields['task_category_id'].choices = SELECT + tuple(categories_as_choices())
    project = forms.ModelChoiceField(queryset=Projects.objects.filter(deleted_at=None), empty_label="Select", label=False)        
   
    task_duration = forms.CharField(label=False,)
    class Meta:
        model = Tasks
        fields = ['user','qc','tl','task_category_id','project','task_duration']    

                      