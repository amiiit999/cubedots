from django.db import models
from django.utils import timezone

from crm_cubedots.model.account import Account
from crm_cubedots.model.departments import Departments

class LeaveTypes(models.Model):
    # Create your models here.
    name                = models.CharField(max_length=50)
    status              = models.CharField(max_length=50,null=True,blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    deleted_at          = models.DateTimeField(blank=True, null=True)
      
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    class Meta:
        db_table = "leaves_type"

    def __str__(self):
        return self.name   