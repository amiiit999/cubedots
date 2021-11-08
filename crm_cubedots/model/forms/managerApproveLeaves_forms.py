from django import forms
from django.db import models

from crm_cubedots.model.apply_leaves import ApplyLeave
from crm_cubedots.constants.constants import LEAVES_APPROVAL

class ApproveLeavesForm(forms.ModelForm):
    approval_status = forms.ChoiceField(choices=LEAVES_APPROVAL)
    reason = forms.CharField(widget=forms.Textarea(attrs={'rows': 1,'style': 'height: 80px;','placeholder':'Note'}), required=True,label='Note')
 
    class Meta:
        model = ApplyLeave
        fields = ['approval_status','reason']
