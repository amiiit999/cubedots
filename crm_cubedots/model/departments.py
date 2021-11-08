from django.db import models
from django.utils import timezone

class Departments(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        db_table = "departments"

    def __str__(self):
        return self.name     