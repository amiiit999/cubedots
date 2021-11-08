from django.db import models
from django.utils import timezone
from crm_cubedots.model.project_categories import ProjectsCategories
class Projects(models.Model):
    # Create your models here.
    project_category = models.ForeignKey(ProjectsCategories,on_delete=models.CASCADE,null=True,related_name='projectCategoryId')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    status = models.CharField(max_length=200)
    started_at = models.DateTimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
      
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
    
    class Meta:
        db_table = "projects"
     
    def __str__(self):
        return self.name            
  