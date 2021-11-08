from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from django.contrib.auth.models import Group 
from crm_cubedots.model.task import Tasks
from crm_cubedots.model.projects import Projects

def monitasks(request):
    context = {}
    user = request.user
    query = {}
    try:
        if(user.role == 'tl'):
            query = Tasks.objects.filter(deleted_at=None ,tl_id=user.id,parent_id=0).order_by('project_id').values_list('project_id',flat=True).exclude(process_status='completed').distinct()
        if(user.role == 'qa'):
            query = Tasks.objects.filter(deleted_at=None ,qc_id=user.id,parent_id=0).order_by('project_id').values_list('project_id',flat=True).exclude(process_status='completed').distinct()
    except:
        pass
    context['total_leaves'] = Projects.objects.filter(id__in=query,status=('active')).count()  

    active_projects = Tasks.objects.filter(deleted_at=None,user_id = user.id, process_status = 'assigned', status = 'active',parent_id=0).order_by('project_id').values_list('project_id',flat=True).distinct() 
    
    context['total_active_projects'] = Projects.objects.filter(deleted_at=None,id__in=active_projects).count()

    context['total_completed_tasks'] = Tasks.objects.filter(deleted_at=None,user_id = user.id, process_status = 'completed', parent_id = 0).count()
    #context['total_completed_tasks'] = Projects.objects.filter(id__in=completed_tasks)

    context['total_active_tasks'] = Tasks.objects.filter(deleted_at=None,user_id = user.id, parent_id = 0).exclude(process_status = 'completed').exclude(process_status = 'qc_rejected').count()
    
    context['total_rejected_tasks'] = Tasks.objects.filter(deleted_at=None,user_id = user.id, parent_id = 0, process_status = 'qc_rejected').count()
    return render(request,'moni_task/dashboard/index.html',context)