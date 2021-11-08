from django.db import models
from django.utils import timezone

from crm_cubedots.model.account import Account

class Manager(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,related_name='managerId')
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,related_name='managerUserId')
    created_at        = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at        = models.DateTimeField(auto_now=True,blank=False, null=True)
    # deleted_at        = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "managers"
        

    def __str__(self):
        return self.name  

class TeamLeader(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    tl = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,related_name='TlId')
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True,related_name='TlUserId')
    created_at        = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at        = models.DateTimeField(auto_now=True,blank=False, null=True)
    # deleted_at        = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "team_leaders"
        

    def __str__(self):
        return self.name         