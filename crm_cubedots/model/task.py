from django.db import models
from django.utils import timezone

from crm_cubedots.model.departments import Departments
from crm_cubedots.model.projects import Projects
from crm_cubedots.model.account import Account

from crm_cubedots.model.task_categories import TaskCategories

class Tasks(models.Model):
    parent_id           = models.BigIntegerField(default=0)
    project             = models.ForeignKey(Projects,on_delete=models.CASCADE,null=True,related_name='tasksProjectId', verbose_name="Project Name")
    department          = models.ForeignKey(Departments,on_delete=models.CASCADE,null=True, related_name='tasksDepartmentId', verbose_name='Department Name')
    user                = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='tasksUserId', verbose_name='User Name')
    qc                  = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name='QC Name', related_name='tasksQcId', null=True)
    tl                  = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='tasksTlId', verbose_name='TL Name')
    task_category       = models.ForeignKey(TaskCategories, on_delete=models.CASCADE, null=True, related_name='tasksCatId', verbose_name='Task Categories Name')
    dependency_id       = models.BigIntegerField(default=0)
    is_extra            = models.IntegerField(default=0)
    taskid              = models.CharField(max_length=100)
    name                = models.CharField(max_length=200, null=True, blank=True)
    description         = models.TextField(null=True,blank=True)
    status              = models.CharField(max_length=50)
    priority            = models.CharField(max_length=50,null=True,blank=True)
    process_status      = models.CharField(max_length=100)
    progress            = models.IntegerField(default=0)
    task_started_at     = models.DateTimeField(null=True,blank=True)
    task_ended_at       = models.DateTimeField(null=True,blank=True)
    task_duration       = models.CharField(default=0, null=True, blank=True,max_length=50)
    work_started_at     = models.DateTimeField(null=True,blank=True)
    work_ended_at       = models.DateTimeField(null=True,blank=True)
    work_duration       = models.IntegerField(default=0)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    deleted_at          = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    

    class Meta:
        db_table = "tasks"
        

    def __str__(self):
        return self.taskid  
    
 
    @property
    def children(self):  
        result = Tasks.objects.filter(parent_id = self.id, status="active")
        return result

      
    
    