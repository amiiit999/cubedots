from django.db import models
from django import forms
from django.forms.fields import DateField, datetime

from crm_cubedots.model.account import Account
from crm_cubedots.model.departments import Departments
from crm_cubedots.model.apply_leaves import ApplyLeave
from crm_cubedots.model.leaves_type import LeaveTypes

            
class ApplyLeavesForm(forms.ModelForm):
    leaves_type = forms.ModelChoiceField(queryset=LeaveTypes.objects.filter(deleted_at=None,status='active'),empty_label='Select',label='Leaves Type')
    # user = forms.ModelChoiceField(queryset=Account.objects.filter(deleted_at=None), empty_label="Select", label="User Name")
    # department = forms.ModelChoiceField(queryset=Departments.objects.filter(deleted_at=None),empty_label="Select", label="Department Name")
    # approval_status = forms.ChoiceField(choices=APPROVAL_HR)
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,'style': 'height: 80px;','placeholder':'Reason'}), required=True)
    start_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}),label='From', required=True)
    end_date = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}),label='To',required=True)
    
    class Meta:
        model = ApplyLeave
        fields = ['leaves_type','reason','start_date','end_date']

        