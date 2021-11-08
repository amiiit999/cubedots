from django.db import models
from django.utils import timezone

from crm_cubedots.model.task import Tasks
from crm_cubedots.model.account import Account

class UserTaskStatus(models.Model):
    user                = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, related_name='tasksStatusUserId')
    task                = models.ForeignKey(Tasks, on_delete=models.CASCADE, null=True, related_name='statusTaskID', verbose_name='Task ID')
    status              = models.CharField(max_length=50)
    note                = models.TextField(max_length=50,blank=True, null=True)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    deleted_at          = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        db_table = "user_task_status"

   