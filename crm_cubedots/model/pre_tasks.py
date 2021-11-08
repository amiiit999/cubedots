from django.db import models
from django.utils import timezone

from crm_cubedots.model.departments import Departments

from crm_cubedots.model.task_categories import TaskCategories

class PreTasks(models.Model):
    parent_id       = models.IntegerField(default=0)
    department      = models.ForeignKey(Departments,on_delete=models.CASCADE,null=True, related_name='preTasksDepartmentId', verbose_name='Department Name')
    task_category   = models.ForeignKey(TaskCategories, on_delete=models.CASCADE, null=True, related_name='preTasksCatId', verbose_name='Task Category Name')
    taskid          = models.CharField(max_length=100)
    name            = models.CharField(max_length=200, null=True, blank=True)
    description     = models.TextField(null=True,blank=True)
    required_time   = models.IntegerField(default=0,null=True,blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    deleted_at      = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    

    class Meta:
        db_table = "pre_tasks"

    def __str__(self):
        return self.department.name