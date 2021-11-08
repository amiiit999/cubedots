from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.contrib import messages
from django import template
from django.db.models import query
from django.core import serializers
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse

#from crm_cubedots.serializers import TaskSerializer
#from itertools import chain
from crm_cubedots.model.task import Tasks
from crm_cubedots.model.projects import Projects
from crm_cubedots.model.task_categories import TaskCategories
from crm_cubedots.model.account import Account
from crm_cubedots.model.forms.adminTasks_forms import AdminTasksForm
import json as JSON





def tasks_index(request,id):
    context = {}
    
    
    context['child_button'] = Tasks.objects.filter(project_id=id, deleted_at=None).exclude(parent_id = 0).values('parent_id').order_by('parent_id').distinct()
    context['subtasks'] =     Tasks.objects.filter(project_id=id, deleted_at=None).exclude(parent_id = 0)
    #context['tasks'] = Tasks.objects.filter(project_id=id ,parent_id = 0 )
    #data5 = Tasks.objects.filter(project_id=id ,parent_id = 0 )
    context['project_add'] = Projects.objects.get(id=id)
    try:
        context['project'] = Tasks.objects.get(id=id)
    except:
        go = None
    
    #print(data5)
    #context['project'] = Tasks.objects.filter(project_id=id).only('project_id').order_by('project_id').first()
    objects_data = Tasks.objects.filter(project_id=id ,parent_id = 0 ,deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
    

    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request,'admin/tasks/index.html',context) 
    #for m['sss'] in child1:
    #   child['child'] = m
    #context['result'] = {'parent':parent, 'child':child}
    #context['data'] = zip(distinct,parent)
   # data2 = list(chain(parent,child))
    #context['data'] = list(chain(parent,child))
   
    #data5 = list(zip(parent, child))
    #['message'] = serializers.serialize('json', data5)
    #context = { 'objects' : parent }
    #response_data['message'] = serializers.serialize('json', data5)
    #return JsonResponse(response_data,safe=False)
    
    #return render(request,'admin/tasks/apis.html',{'data5':data5})

def tasks_create(request,id):
    #taskids = Tasks.objects.filter(parent_id=0, project_id = id).values_list('id', 'taskid').order_by('name')
    
    context = {}
    project = Projects.objects.get(id=id)
    context['row'] = project
    context['form'] = AdminTasksForm(parent_id_arg = project.id)    
    return render(request,'admin/tasks/create.html',context)

def tasks_store(request,id): 
    Context = {}
    project = Projects.objects.get(id=id)
    
    form = AdminTasksForm(request.POST or None, parent_id_arg = project.id )
    
    if form.is_valid():
        
        instance = form.save(commit=False)
        instance.user_id = request.POST['user']
        instance.department_id = request.POST['department']
        instance.tl_id = request.POST['tl']
        instance.qc_id = request.POST['qc']
        instance.task_category_id = request.POST['task_category']
        instance.parent_id = request.POST['parent_id']
        instance.user_id = request.POST['user']
        instance.project_id = project.id
        
        instance.save()
        messages.success(request, 'Task Added Successfully !! ')
        Context['row'] = project
        Context['form'] = form
        return redirect('admin_task_index', id=id)
    else:
        Context['row'] = project
        Context['form'] = form
        return render(request, 'admin/tasks/create.html', Context)          
     
def tasks_search(request,id):
    context = {}
    context['project'] = Tasks.objects.get(id=id)
    return_id = Tasks.objects.get(id=id)
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
       
        context['page_obj'] = Tasks.objects.filter(Q(taskid__icontains=query) | Q(name__icontains=query) | Q(process_status__icontains=query) , project_id=id,  deleted_at=None)
        return render(request,'admin/tasks/index.html', context)
        
    else:
        return redirect("admin_task_index", id=return_id.project_id)    


def tasks_show(request,id):
    context = {}
    
    context['task'] = Tasks.objects.get(id=id)
   
    return render(request, 'admin/tasks/show.html',context)

def tasks_update(request,id):
    context = {}
    update = Tasks.objects.get(id=id)
    
    form = AdminTasksForm(request.POST or None, instance=update, parent_id_arg = update.project_id)
    if form.is_valid():
            form.save()
            messages.success(request, 'Task Updated Successfully !! ')
            return redirect('admin_task_index', id=update.project_id)
    else:    
        context['row'] = Tasks.objects.get(id=id)
        context['form'] = form
    return render(request, 'admin/tasks/edit.html', context)   

def tasks_soft_delete(request,id):
    delete_id = Tasks.objects.get(id=id)
    Tasks.objects.get(id=id).soft_delete()
    messages.success(request, 'Task Deleted Successfully !! ')
    return redirect('admin_task_index', id=delete_id.project_id)

def json(request):
    response_data = {}
    data =  Tasks.objects.all()
    response_data = serializers.serialize('json', data)
    data = JSON.loads(response_data)
    return JsonResponse(data,safe=False)