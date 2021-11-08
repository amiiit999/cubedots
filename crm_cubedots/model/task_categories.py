from django.db import models
from django.utils import timezone
from crm_cubedots.constants.constants import PARENT_ID

from crm_cubedots.model.departments import Departments


class TaskCategories(models.Model):
    
    department = models.ForeignKey(Departments,on_delete=models.CASCADE,null=True,related_name='departmentId')
    parent_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
        
    class Meta:
        db_table = "task_categories"

    def __str__(self):
        return self.name
