from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from django.contrib.auth.models import Group 

from crm_cubedots.model.task import Tasks
from crm_cubedots.model.projects import Projects

login_required(login_url='login')
def user_dashboard_index(request):
    context = {}
    user = request.user

    active_projects = Tasks.objects.filter(deleted_at=None, user_id = user.id, process_status = 'assigned', status = 'active').order_by('project_id').values_list('project_id',flat=True).distinct()
    context['total_active_projects'] = Projects.objects.filter(deleted_at=None,id__in=active_projects,status='active').count()

    context['total_completed_tasks'] = Tasks.objects.filter(deleted_at=None,user_id = user.id, process_status = 'completed', parent_id = 0).count()
    #context['total_completed_tasks'] = Projects.objects.filter(id__in=completed_tasks)

    context['total_active_tasks'] = Tasks.objects.filter(deleted_at=None,user_id = user.id, parent_id = 0).exclude(process_status = 'completed').exclude(process_status = 'qc_rejected').count()
    
    context['total_rejected_tasks'] = Tasks.objects.filter(deleted_at=None,user_id = user.id, parent_id = 0, process_status = 'qc_rejected').count()
    
    #print("active_tasks",active_tasks)
    #context['total_active_tasks'] = Tasks.objects.filter(id__in=active_tasks)
    
    
    return render(request,'users/dashboard/index.html',context)