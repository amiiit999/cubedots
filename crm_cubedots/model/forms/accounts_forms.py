from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.forms.fields import DateField, datetime

#---CONSTANTS -------
from crm_cubedots.constants.constants import USER_ROLE
from crm_cubedots.constants.constants import ACTIVE_STATUS
from crm_cubedots.constants.constants import GENDER
from crm_cubedots.constants.constants import APPROVAL_ADMIN
from crm_cubedots.constants.constants import APPROVAL_HR
from crm_cubedots.constants.constants import BLOOD_GROUPS


from crm_cubedots.model.departments import Departments
from crm_cubedots.model.account import Account

from django.db.models import Q

class AccountShortForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    department = forms.ModelChoiceField(queryset=Departments.objects.all(), empty_label="Select Department")
    status = forms.ChoiceField(choices = ACTIVE_STATUS)
    gender = forms.ChoiceField(choices = GENDER)
    role = forms.ChoiceField(choices=USER_ROLE)
    date_joined = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    
 
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','role','department','status','gender','date_joined']
        

class AccountsForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    department = forms.ModelChoiceField(queryset=Departments.objects.filter(deleted_at = None), empty_label="Select Department")
    status = forms.ChoiceField(choices = ACTIVE_STATUS)
    gender = forms.ChoiceField(choices = GENDER)
    role = forms.ChoiceField(choices=USER_ROLE)
    date_joined = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    approval_status = forms.ChoiceField(choices=APPROVAL_HR)
    date_of_birth = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    team_leader = forms.ModelChoiceField(queryset=Account.objects.filter(Q(role='tl') | Q(role='qa')).order_by('id'), empty_label="Select")
    
    manager_name = forms.ModelChoiceField(queryset=Account.objects.filter(Q(role='tl') | Q(role='qa')), empty_label="Select")
    blood_group = forms.ChoiceField(choices = BLOOD_GROUPS)
    
    class Meta:
       model = Account
       fields = ['email','first_name','last_name','date_joined','gender','role','date_of_birth','designation','contact_no','department','team_name','team_leader','manager_name','status','blood_group','local_address','permanent_address','skills','qualifications','postal_code','approval_status']
   
class AccountsProfilePicForm(forms.ModelForm):
   
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'onchange': 'this.form.submit();','id':'upload-photo'}))
   
    class Meta:
       model = Account
       fields = ['avatar']

class AccountResetPasswordForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['password1','password2']


