from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tablib import Dataset
import xlwt
import datetime

#from crm_cubedots.serializers import TaskSerializer
#from itertools import chain
from crm_cubedots.model.task import Tasks
from crm_cubedots.model.projects import Projects
from crm_cubedots.model.task_categories import TaskCategories
from crm_cubedots.model.account import Account

from crm_cubedots.model.forms.pre_tasks_forms import PreTasksForm
from crm_cubedots.model.pre_tasks import PreTasks
from crm_cubedots.model.departments import Departments
from crm_cubedots.model.forms.departements_forms import DepartmentSelectForm
from crm_cubedots.model.forms.pre_tasks_forms import ExportTasks

def pretasks_index(request):
    context= {}
    objects_data = PreTasks.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,30) # Show 10 contacts per page.
    context['department'] = Departments.objects.filter(deleted_at=None)
    
     
    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request,'admin/pre_tasks/index.html',context)

def pretask_create(request):
    Context = {}
    Context['form'] = PreTasksForm()
    return render(request, 'admin/pre_tasks/create.html',Context)

def pretask_store(request):

    if request.method == "POST":
        
        form = PreTasksForm(request.POST or None)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Task Added Successfully !! ')
                return redirect("pretasks_index")
            
            except:
                pass
                messages.error(request, 'Failed')
            return render(request, 'admin/pre_tasks/create.html', {'form': form})  

def pretask_update(request,id):         
    update = PreTasks.objects.get(id=id)
    Context = {}
    form = PreTasksForm(request.POST or None, instance=update)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'PreTask Updated Successfully !! ')
            return redirect("pretasks_index")
        except:
            pass
    else:    
        Context['form'] = form
        return render(request, 'admin/pre_tasks/edit.html', Context)   

def pretask_soft_deleted(request,id):
    PreTasks.objects.get(id=id).soft_delete()
    messages.success(request, 'PreTasks Task Deleted Successfully !! ')
    return redirect('pretasks_index')

@login_required(login_url='login')

def pretask_search(request):
    context = {}
   
    if request.GET.get('search'):
        if request.method == 'GET': # this will be GET now      
            query =  request.GET.get('search') # do some research what it does       
            context['page_obj'] = PreTasks.objects.filter(Q(name__icontains=query) | Q(taskid__icontains=query),deleted_at=None)
            return render(request,'admin/pre_tasks/index.html', context)
    else:
        return redirect("pretasks_index",context)  

def pretask_create_bulk_index(request):
    context = {}
    context['deptform']= DepartmentSelectForm(request.POST)
   
    context['qc'] = Account.objects.filter(Q(role='tl') | Q(role='qa'))
    context['tl'] = Account.objects.filter(role='tl')
    context['users'] = Account.objects.filter(deleted_at = None)
    context['projects'] = Projects.objects.filter(deleted_at = None)
    #context['task_categories'] = tuple(categories_as_choices())
    
    context['task_categories'] = TaskCategories.objects.filter(deleted_at = None)

    

    query =  request.POST.get('department')
   
    if request.POST.get('department'):
        if request.method == 'POST': # this will be GET now      
            query =  request.POST.get('department') # do some research what it does       
            context['page_obj'] = PreTasks.objects.filter(department=query,parent_id = 0, deleted_at=None)
            context['child_button'] = PreTasks.objects.filter(department=query, deleted_at=None).exclude(parent_id=0).values('parent_id').order_by('parent_id').distinct()
            context['subtasks'] =  PreTasks.objects.filter(department=query, deleted_at=None).exclude(parent_id=0)               
            return render(request,'admin/pre_tasks/create_bulk.html', context)
                    
    else:
        return render(request,'admin/pre_tasks/create_bulk.html', context)   

def pretask_create_bulk_search(request):
    context = {}
    context['qc'] = Account.objects.filter(Q(role='tl') | Q(role='qa'))
    context['tl'] = Account.objects.filter(role='tl')
    context['users'] = Account.objects.filter(deleted_at = None)
    context['projects'] = Projects.objects.filter(deleted_at = None)
    context['task_categories'] = TaskCategories.objects.filter(deleted_at = None)
    context['deptform']= DepartmentSelectForm(request.GET)
    context['departments'] = PreTasks.objects.filter(deleted_at = None)
    if request.GET.get('search'):
        if request.method == 'GET': # this will be GET now      
            query =  request.GET.get('search') # do some research what it does       
            context['page_obj'] = PreTasks.objects.filter(Q(name__icontains=query) | Q(taskid__icontains=query),deleted_at=None)        
            
            """page = request.GET.get('page', 1)
            paginator = Paginator(objects_data,10) # Show 10 contacts per page
            try:
                context['page_obj'] = paginator.page(page)
            except PageNotAnInteger:
                context['page_obj'] = paginator.page(1)
            except EmptyPage:
                context['page_obj'] = paginator.page(paginator.num_pages)"""
            return render(request,'admin/pre_tasks/create_bulk.html', context)   
    else:
        return render(request,'admin/pre_tasks/create_bulk.html', context)

def pretask_create_bulk_store(request):
        action = []
        context = {}
        if request.method == "POST":
            context['deptform']= DepartmentSelectForm(request.POST)
            #form = PreTasksCreateBulkForm(request.POST)
            action = request.POST.getlist('action[]')
            
            
            if action:
                for validation_id in action:
                   
                    if ((request.POST['user_id['+validation_id+']']) and (request.POST['tl_id['+validation_id+']']) and (request.POST['qc_id['+validation_id+']']) and (request.POST['project_id['+validation_id+']']) and (request.POST['task_duration['+validation_id+']']) and (request.POST['task_category_id['+validation_id+']'])and (request.POST['task_started_at['+validation_id+']'])and (request.POST['task_ended_at['+validation_id+']'])and (request.POST['priority['+validation_id+']']) ):   
                        for pre_task_id in action:
                           
                            preTasks = PreTasks.objects.filter(id = pre_task_id).first()
                                
                            subtasks = PreTasks.objects.filter(parent_id = preTasks.id)
                            #data = request.POST("user_id[pre_task_id]", "qc_id[pre_task_id]","tl_id[pre_task_id]","project_id[pre_task_id]","task_duration","task_category_id[pre_task_id]")
                            #print("check",request.POST('user_id[pre_task_id]'))
                                
                            if preTasks:                    
                                PreTask = Tasks.objects.create(
                                taskid          =   preTasks.taskid,
                                name            =   preTasks.name,
                                description     =   preTasks.description,
                                status          =   'active',
                                priority        =   request.POST['priority['+pre_task_id+']'],
                                process_status  =   'assigned',
                                parent_id       =   0,
                                department_id   =   preTasks.department_id,
                                user_id         =   request.POST['user_id['+pre_task_id+']'],
                                tl_id           =   request.POST['tl_id['+pre_task_id+']'],
                                qc_id           =   request.POST['qc_id['+pre_task_id+']'],
                                project_id      =   request.POST['project_id['+pre_task_id+']'],
                                task_started_at =   request.POST['task_started_at['+pre_task_id+']'],
                                task_ended_at   =   request.POST['task_ended_at['+pre_task_id+']'],
                                task_duration   =   request.POST['task_duration['+pre_task_id+']'],
                                task_category_id=   request.POST['task_category_id['+pre_task_id+']']                    
                                )
                                    
                                if subtasks:
                                    for tasks in subtasks: 
                                        print("pre_task_id",pre_task_id)   
                                        Tasks.objects.create(
                                            taskid              =   tasks.taskid,
                                            name                =   tasks.name,
                                            description         =   tasks.description,
                                            status              =   'active',
                                            priority            =   request.POST['priority['+pre_task_id+']'],
                                            process_status      =   'assigned',
                                            parent_id           =   PreTask.id,
                                            department_id       =   PreTask.department_id,
                                            user_id             =   request.POST['user_id['+pre_task_id+']'],
                                            tl_id               =   request.POST['tl_id['+pre_task_id+']'],
                                            qc_id               =   request.POST['qc_id['+pre_task_id+']'],
                                            project_id          =   request.POST['project_id['+pre_task_id+']'],
                                            task_duration       =   request.POST['task_duration['+pre_task_id+']'],
                                            task_started_at     =   request.POST['task_started_at['+pre_task_id+']'],
                                            task_ended_at       =   request.POST['task_ended_at['+pre_task_id+']'],
                                            task_category_id    =   request.POST['task_category_id['+pre_task_id+']']
                                            )
                        messages.success(request, 'Task(s) Added Successfully !! ')
                        return redirect("pretask_createBulk_index") 
                    else:
                        messages.error(request, 'Please fill in required fields !! ')
                    return redirect("pretask_createBulk_index") 
        
def pretask_upload_sheet_store(request):
    if request.method == 'POST':
        dataset = Dataset()
        data_sheet = request.FILES['excel_sheet_file']

        imported_data = dataset.load(data_sheet.read(),format='xlsx')
        print("imported_data",imported_data)
        for data in imported_data:
        	PreTasks.objects.create(
                id              =   data[0],
        		parent_id       =   data[1],
                department_id   =   data[2],
                task_category_id=   data[3],
        		taskid          =   data[4],
        		name            =   data[5],
        		description     =   data[6],
                required_time   =   data[7]              
                )      
    messages.success(request, 'PreTaks(s) Added Successfully !! ')
    return redirect('pretasks_index')

def pretask_upload_sheet_index(request):
    context = {}
    context['preTask_last_id'] = PreTasks.objects.last()
    return render(request,'admin/pre_tasks/upload_tasks.html', context)

def pretask_export_tasks(request):
    today_date =  datetime.date.today()
    project_id = request.POST['project']
    #project_name = Projects.objects.get(id=project_id)
    #print("name = ",project_name.name)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="project_'+project_id+'_task_'+ str(today_date) +'.xlsx"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Worksheet')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id','parent_id','user_id','tl_id','department_id','task_category_id','qc_id','project_id','taskid','name','description','is_extra','dependency_id','status','process_status','progress','task_started_at','task_ended_at','task_duration','work_started_at','work_ended_at','work_duration','created_at','updated_at','deleted_at']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    
    rows = Tasks.objects.filter(project_id=project_id).values_list('id','parent_id','user_id','tl_id','department_id','task_category_id','qc_id','project_id','taskid','name','description','is_extra','dependency_id','status','process_status','progress','task_started_at','task_ended_at','task_duration','work_started_at','work_ended_at','work_duration','created_at','updated_at','deleted_at')
    rows = [[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime.datetime) else x for x in row] for row in rows ]
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response    

def pretask_export_tasks_index(request):
    context ={}
    context['form'] = ExportTasks()
    return render(request,'admin/pre_tasks/download_tasks.html',context)    

def categories_as_choices():
    categories = []
    for category in TaskCategories.objects.only('id','name').filter(parent_id=0).order_by('name'):
        new_category = []
        sub_categories = []
        for sub_category in TaskCategories.objects.filter(parent_id = category.id):
            sub_categories.append([sub_category.id, sub_category.name])

        new_category = [category, sub_categories]
        categories.append(new_category)

    return categories    

      
    


    