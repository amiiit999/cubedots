from django.db import models
from django.utils import timezone

from crm_cubedots.model.account import Account
from crm_cubedots.model.departments import Departments
from crm_cubedots.model.leaves_type import LeaveTypes
from crm_cubedots.model.manager import Manager
from crm_cubedots.model.manager import TeamLeader

class ApplyLeave(models.Model):
    # Create your models here.
    leaves_type         = models.ForeignKey(LeaveTypes, on_delete=models.CASCADE,null=True, related_name='leavesTypeId', verbose_name='Leaves Type')
    user                = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, verbose_name='Employee Name')
    department          = models.ForeignKey(Departments, on_delete=models.CASCADE, null=True, verbose_name='Department Name')
    approval_status     = models.CharField(verbose_name="Approval Status", max_length=60, null=True)
    tl_approval         = models.CharField(verbose_name="Tl Approval Status", max_length=60, null=True)
    manager_approval    = models.CharField(verbose_name="Manager Approval Status", max_length=60, null=True)
    manager             = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='Manager Name', related_name='leavesTypeManagerId', null=True)
    tl                  = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='leavesTypeTlId', verbose_name='TL Name')
    reason              = models.TextField(verbose_name="Reason")
    start_date          = models.DateTimeField(verbose_name="From",null=True,blank=True)
    end_date            = models.DateTimeField(verbose_name="To",null=True,blank=True)
    total               = models.CharField(null=True,blank=True,max_length=50)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    deleted_at          = models.DateTimeField(blank=True, null=True)
      
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    class Meta:
        db_table = "leaves_applied"

    def __str__(self):
        return self.leaves_type.name