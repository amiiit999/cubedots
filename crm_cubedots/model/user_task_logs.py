from django.db import models
from django.utils import timezone

from crm_cubedots.model.task import Tasks
from crm_cubedots.model.account import Account

class UserTaskLog(models.Model):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='tasksLogUserId')
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=True, related_name='taskID', verbose_name='Task ID')
    work_duration       = models.IntegerField(default=0)
    work_started_at     = models.DateTimeField(null=True,blank=True)
    work_ended_at       = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        db_table = "user_task_logs"
