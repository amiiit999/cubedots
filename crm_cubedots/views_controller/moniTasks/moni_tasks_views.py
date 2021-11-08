from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from django.db.models import Q
from django.contrib.auth.models import Group 

from crm_cubedots.model.projects import Projects
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound,Http404
from json import dumps
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied
from django.utils.functional import SimpleLazyObject
from django.core import serializers
from django.core.serializers import serialize
import json
from django.db.models import Avg, Count, Min, Sum, Max
import datetime

from crm_cubedots.constants import constants
from crm_cubedots.model.user_task_logs import UserTaskLog
from crm_cubedots.model.user_task_status import UserTaskStatus
from crm_cubedots.model.task import Tasks

def moni_tasks_index(request):
    template_name = 'moni_task/tasks/index.html'
    query = []
    user = request.user
    
    if(user.isTl or user.isTlQa):
        query = Tasks.objects.filter(deleted_at=None ,tl_id=user.id,parent_id=0).order_by('project_id').values_list('project_id',flat=True).exclude(process_status='completed').distinct()
    elif(user.isQa or user.isTlQa):
        query = Tasks.objects.filter(deleted_at=None,qc_id=user.id,parent_id=0).order_by('project_id').values_list('project_id',flat=True).exclude(process_status='completed').distinct()
    else:
        return HttpResponse('Unauthorized', status=401)
    objects_data = Projects.objects.filter(id__in=query,status=('active'))  
    
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
   
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request, template_name,{'page_obj': page_obj})

def moni_tasks_search(request):
    context = {}
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        try:
            
            
            context['page_obj'] = Projects.objects.filter(Q(name__icontains=query) | Q(status__icontains=query), deleted_at=None)
            return render(request,'moni_task/tasks/index.html', context)
        except:
                pass
    else:
        return redirect("moni_task_index")   

def moni_tasks_showProjects(request,id):
    
    user = request.user
    task = Tasks.objects.get(id=id)
    query = {}
    data=[]
    context = {}
   
    if(user.isTlQa or user.isQa):
        taskStatusListAccess = constants.qa_task_process_status_list_access
        taskStatusTimerViewAccess = constants.qa_task_process_status_timer_view_access
    elif(user.isUser):
        taskStatusListAccess = constants.user_task_process_status_list_access
        taskStatusTimerViewAccess = constants.user_task_process_status_timer_view_access
    elif(user.isTl):
        taskStatusListAccess = constants.tl_task_process_status_list_access
        taskStatusTimerViewAccess = constants.tl_task_process_status_timer_view_access
    else:
        pass

    if(user.isTl or user.isTlQa):
        query = Tasks.objects.filter(tl_id=user.id,project_id=id).order_by('project_id').values_list('project_id', flat=True).distinct()
        
    elif(user.isQa or user.isTlQa):
        query = Tasks.objects.filter(qc_id=user.id,project_id=id).order_by('project_id').values_list('project_id', flat=True).distinct()
    else:
        return HttpResponseNotFound("Not Found") 

    project = Projects.objects.filter(id__in=query).first()

    if(not project):
        raise PermissionDenied
    elif(project.status != 'active'):
        return HttpResponseNotFound("Sorry! project status is not active.") 

    if(user.isTl):
        userWhere = 'tl_id'
    elif(user.isQa or user.isTlQa):
        userWhere = 'qc_id'
    else:
        return HttpResponseNotFound("This user role not permitted.")     
    
    taskQuerySet = Tasks.objects.filter(**{ userWhere: user.id } ,parent_id=0, status="active", project_id=id).exclude(user_id=user.id)     
    testQuery = taskQuerySet.filter(process_status__in = taskStatusTimerViewAccess)
    
    tasksStatics = Tasks.objects.filter(**{ userWhere: user.id } ,parent_id=0, status="active", project_id=id)
    context['totalTasksStatics'] = tasksStatics.filter(deleted_at=None,parent_id=0).count()

    context['tasksStaticsAssigned'] = tasksStatics.filter(deleted_at=None,process_status="assigned",parent_id=0).aggregate(assigned = Count("process_status"))

    context['tasksStaticsTlRejected'] = tasksStatics.filter(deleted_at=None,process_status="tl_rejected",parent_id=0).aggregate(tl_rejected = Count("process_status"))

    context['tasksStaticsQaRejected'] = tasksStatics.filter(deleted_at=None,process_status="qc_rejected",parent_id=0).aggregate(qa_rejected = Count("process_status"))

    context['tasksStaticsCompleted'] = tasksStatics.filter(deleted_at=None,process_status="completed",parent_id=0).aggregate(completed = Count("process_status"))

    if(user.isTl):
        context['tasksStatics'] = tasksStatics.filter(deleted_at=None,process_status__in={'tl_started','forwarded_to_tl'},parent_id=0).aggregate(tasks = Count("process_status"))
    elif(user.isQa):
        context['tasksStatics'] = tasksStatics.filter(deleted_at=None,process_status__in={"qc_started","forwarded_to_qc"},parent_id=0).aggregate(tasks = Count("process_status"))         
    else:
        return HttpResponseNotFound("This user role does not have access permission.") 

    context['project'] = Projects.objects.get(id=id)
    

    objects_data = testQuery.order_by("-created_at")
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.

    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)

    return render(request,'moni_task/tasks/showProjects.html',context)

def moni_tasks_showProjects_search(request,id):
    context = {}
    user = request.user
    context['project'] = Projects.objects.get(id=id)
    if(user.isTl or user.isTlQa):
        query = Tasks.objects.filter(tl_id=user.id,project_id=id).order_by('project_id').values_list('project_id', flat=True).distinct()
    elif(user.isQa or user.isTlQa):
        query = Tasks.objects.filter(qc_id=user.id,project_id=id).order_by('project_id').values_list('project_id', flat=True).distinct()
    else:
        return HttpResponseNotFound("Not Found") 

    project = Projects.objects.filter(id__in=query).first()

    if (not project):
        raise PermissionDenied

    if (project.status != 'active'):
        raise PermissionDenied    

    if(user.isTl):
        userWhere = 'tl_id'
    elif(user.isQa or user.isTlQa):
        userWhere = 'qc_id'
    else:
        return HttpResponseNotFound("This user role not permitted.")  
    
    tasksStatics = Tasks.objects.filter(**{ userWhere: user.id } ,parent_id=0, status="active", project_id=id)
    context['totalTasksStatics'] = tasksStatics.filter(parent_id=0).count()

    context['tasksStaticsAssigned'] = tasksStatics.filter(process_status="assigned",parent_id=0).aggregate(assigned = Count("process_status"))

    context['tasksStaticsTlRejected'] = tasksStatics.filter(process_status="tl_rejected",parent_id=0).aggregate(tl_rejected = Count("process_status"))

    context['tasksStaticsQaRejected'] = tasksStatics.filter(process_status="qc_rejected",parent_id=0).aggregate(qa_rejected = Count("process_status"))

    context['tasksStaticsCompleted'] = tasksStatics.filter(process_status="completed",parent_id=0).aggregate(completed = Count("process_status"))

    if(user.isTl):
        context['tasksStatics'] = tasksStatics.filter(process_status__in={'tl_started','forwarded_to_tl'},parent_id=0).aggregate(tasks = Count("process_status"))
    elif(user.isQa):
        context['tasksStatics'] = tasksStatics.filter(process_status__in={"qc_started","forwarded_to_qc"},parent_id=0).aggregate(tasks = Count("process_status"))         
    else:
        return HttpResponseNotFound("This user role does not have access permission.") 

    if request.method == 'GET': # this will be GET now      
                query =  request.GET.get('search') # do some research what it does       
                try:
                
                    context['page_obj'] = Tasks.objects.filter(Q(taskid__icontains=query) | Q(name__icontains=query) | Q(status__icontains=query),project_id = id, deleted_at=None,status = 'active', parent_id = 0)
                    return render(request,'moni_task/tasks/showProjects.html', context)
                except:
                        pass
    else:
        return redirect("user_tasks")

def moni_tasks_show(request,id):
    user = request.user
    taskQuery = {}
    taskStatusListAccessData = []
    taskStatusTimerViewAccessData =[]
    data =[]
    if(user.isTlQa or user.isQa):
        taskStatusListAccess = constants.qa_task_process_status_list_access
        taskStatusTimerViewAccess = constants.qa_task_process_status_timer_view_access
    elif(user.isUser):
        taskStatusListAccess = constants.user_task_process_status_list_access
        taskStatusTimerViewAccess = constants.user_task_process_status_timer_view_access
    elif(user.isTl):
        taskStatusListAccess = constants.tl_task_process_status_list_access
        taskStatusTimerViewAccess = constants.tl_task_process_status_timer_view_access
    else:
        pass

    taskStatusListAccessData = json.dumps(taskStatusListAccess)
    taskStatusTimerViewAccessData = json.dumps(taskStatusTimerViewAccess)
  
    tasks = Tasks.objects.filter(id=id)
    
    taskQuerySet = tasks.filter(process_status__in=taskStatusTimerViewAccess)

    userColumnId = 'id'
    if(user.isTl):
        taskQuery = taskQuerySet.filter(tl_id=user.id)
        userColumnId = 'tl_id'
    elif(user.isTlQa or user.isQa):
        taskQuery = taskQuerySet.filter(qc_id = user.id)
        userColumnId = 'qc_id'
    else:
        return HttpResponseNotFound("Invalid User Role.")         
    
    task = taskQuery.first()
    task_data = serializers.serialize("json",[task])

    if(not task):
        return HttpResponseNotFound("task not found") 

    taskPrevious = Tasks.objects.filter(**{userColumnId:user.id},project_id = task.project_id,id__lt = task.id).order_by('-id').first()

    taskNext = Tasks.objects.filter(**{userColumnId:user.id},project_id = task.project_id,id__gt = task.id).order_by('id').first()

    project = Projects.objects.filter(id=task.project_id).first()

    if(not project):
        return HttpResponseNotFound("task project not found.") 
    if(project.status != 'active'):
        return HttpResponseNotFound("Unauthorized, project is not active.") 

    if(user.isTl):
        if(task.tl_id == user.id and task.qc_id == user.id):
            taskStatusListAccess = [
                {'tl_started' : "start"},
                {'completed' : "completed"},
                ]
            
            taskStatusTimerViewAccess = [
            'tl_started',
            'forwarded_to_tl'
            ]
            taskStatusListAccessData = json.dumps(taskStatusListAccess)
            taskStatusTimerViewAccessData = json.dumps(taskStatusTimerViewAccess)
    
    return render(request, 'moni_task/tasks/show.html',{'task_data':task_data,'task':task,'taskStatusListAccessData':taskStatusListAccessData,'taskStatusTimerViewAccessData':taskStatusTimerViewAccessData,'taskNext':taskNext,'taskPrevious':taskPrevious})

def moni_tasks_getAjaxTask(request,id):
    user = request.user
    task = Tasks.objects.get(id=id)
    taskSerialize=[]
    nowStartTime = datetime.datetime.now()
    todayDate = nowStartTime.strftime("%m-%d-%Y")
    if(user.isTl):
        userWhere =  'tl_id'
    elif(user.isQa or isTlQa):
        userWhere = 'qc_id'
    else:
        raise PermissionDenied

    taskQuery = Tasks.objects.filter(id=task.id,**{userWhere:user.id}).first()

    taskSerialize = serializers.serialize("json", [taskQuery])
    tasks = json.loads(taskSerialize)

    subTasksQuery = Tasks.objects.filter(parent_id=task.id,**{userWhere:user.id}).order_by('id')
    subTasksSerialize = serializers.serialize("json", subTasksQuery)
    subTasks = json.loads(subTasksSerialize)
    return JsonResponse({'task':tasks,'subTask':subTasks,'todayDate':todayDate})

def moni_tasks_getAjaxTaskLog(request,id):
    user = request.user
    nowStartTime = datetime.datetime.now()
    task = Tasks.objects.get(id=id)

    todaydurations = UserTaskLog.objects.filter(user_id=user.id, task_id=task.id, created_at__date=nowStartTime.strftime("%Y-%m-%d")).aggregate(Sum('work_duration'))
    taskLogs = UserTaskLog.objects.filter(task_id = task.id,user_id=user.id).order_by('-created_at')
    
    taskLogsSerialize = serializers.serialize("json", taskLogs)
    tasks = json.loads(taskLogsSerialize)

    todayduration = todaydurations['work_duration__sum']
    
    return JsonResponse({'task':tasks,'todayduration':todayduration}) 

def moni_tasks_getAjaxTaskStatus(request,id):
    user = request.user
    nowStartTime = datetime.datetime.now()
    task = Tasks.objects.get(id=id)
    taskStatus = list(UserTaskStatus.objects.filter(task_id=task.id).order_by('-created_at').values())
    # taskStatusSerialize = serializers.serialize("json", taskStatus)
    # tasks = json.loads(taskStatusSerialize)

    # userSerialize = serializers.serialize("json", [user])
    # user = json.loads(userSerialize)
    return JsonResponse({'taskStatus':taskStatus},safe=False)
    
def moni_tasks_storeTime(request,id):
    
    user = request.user
    userTaskLog = []

    task = Tasks.objects.get(id=id)
    taskProcessStatusList = []
    if(not user.isTl and not user.isQa and not user.isTlQa):
        return JsonResponse({'error':'Unauthorized access'}, status_code=401)

    taskProcessStatusList = constants.USER_TASK_PROCESS_STATUS
    nowStartTime = datetime.datetime.now()

    statusData = []

    if(user.isTl):
        statusData = taskProcessStatusList['tl_started']
    elif(user.isQa or user.isTlQa):
        statusData =  taskProcessStatusList['qc_started']   
    else:
        raise PermissionDenied

    userTaskLogData = UserTaskLog.objects.create(
        user_id         = user.id,
        task_id         = task.id,
         work_started_at = nowStartTime
    )

    userTaskLogDataSerialize = serializers.serialize("json", [userTaskLogData])
    userTaskLog = json.loads(userTaskLogDataSerialize)

    todayDate = nowStartTime.strftime("%m-%d-%Y")

    try:
        taskStatus = UserTaskStatus.objects.filter(user_id=user.id,task_id = task.id).latest('id')
    except:
        taskStatus = None
        

    statusData = {
        'user_id'   : user.id,
        'task_id'   : task.id,
        'status'    : statusData  
    }
    if(taskStatus):
        if(taskStatus.status != statusData['status']):
            UserTaskStatus.objects.create(**statusData) 
    else:
        UserTaskStatus.objects.create(**statusData)

    if(task.parent_id):
        pass
    Tasks.objects.filter(id=task.id).update(process_status=statusData['status'])
  
    return JsonResponse({'tasks':userTaskLog}) 

def moni_tasks_updateTime(request,id):
    
    totalAmonut = []
    date_format = "%Y-%m-%d %H:%M:%S.%f"

    user = request.user
    task = Tasks.objects.get(id=id)

    if(not user.isTl and not user.isQa and not user.isTlQa):
        return JsonResponse({'error':'Unauthorized access'}, status_code=401)

    taskFinishTime = datetime.datetime.now();
    taskLogFinishTime = datetime.datetime.now();

    taskProcessStatusList = constants.USER_TASK_PROCESS_STATUS

    statusData = {
        'user_id'   : user.id,
        'task_id'   : task.id,
    }

    if(user.isTl):
        statusData = taskProcessStatusList['tl_started']
    elif(user.isQa or isTlQa):
        statusData = taskProcessStatusList['qc_started']
    else:
        raise PermissionDenied

    userTaskLogQuery = UserTaskLog.objects.filter(user_id=user.id,task_id=task.id,work_started_at__date=taskLogFinishTime.strftime("%Y-%m-%d")).order_by('-created_at').first()
    userTaskLogSerialize = serializers.serialize("json", [userTaskLogQuery])
    userTaskLog = json.loads(userTaskLogSerialize)
    
    if(userTaskLogQuery):
        taskLogStartTime = userTaskLogQuery.work_started_at

        time_start = str(taskLogStartTime)
        time_end = str(taskLogFinishTime)
        
        diff = datetime.datetime.strptime(time_end, date_format) - datetime.datetime.strptime(time_start, date_format)
        diff_minutes = round(diff.total_seconds() / 60)

    #update task log
        UserTaskLog.objects.filter(id=userTaskLogQuery.id).update(
            work_ended_at = taskLogFinishTime,
            work_duration = diff_minutes
        )

    # totalDurationQuery = UserTaskLog.objects.filter(user_id=user.id,task_id=task.id).aggregate(Sum('work_duration'))
        
        #time = format_timespan(diff_hours)
        
        Tasks.objects.filter(id=task.id).update(
            process_status = statusData,
        )   
        if(task.parent_id):
            pass
            # fromChildTask = Tasks.objects.filter(user_id=user.id,parent_id=task.parent_id).aggregate(Min("work_started_at"), Max("work_ended_at"),Sum("work_duration"))
          
            # if(fromChildTask):
            #         Tasks.objects.filter(id=task.parent_id).update(
            #             work_started_at         = fromChildTask['work_started_at__min'],
            #             work_ended_at           = fromChildTask['work_ended_at__max'],
            #             work_duration           = fromChildTask['work_duration__sum']
            #         );
                
        return JsonResponse({'data':userTaskLog},status=200)

def moni_tasks_updateStatus(request,id):
    inputs = []
   
    data = json.loads(request.body)
    user = request.user
    task = Tasks.objects.get(id=id)
    
    inputs = data   
    inputs['user_id'] = user.id
    inputs['task_id'] = task.id

    if(task.parent_id == 0):
        userTaskStatusQuery = UserTaskStatus.objects.create(**inputs)
        #update parent task
        Tasks.objects.filter(id=task.id).update(
        process_status = inputs['status']
        )

        userTaskStatusDataSerializers = serializers.serialize("json", [userTaskStatusQuery])
        UserTaskStatusData = json.loads(userTaskStatusDataSerializers)

    if(user.isTl):
        if((inputs['status'],'tl_rejected','forwarded_to_qc')):
            Tasks.objects.filter(parent_id=task.id).update(
            process_status = inputs['status'])

            #update sub task
            Tasks.objects.filter(parent_id=task.id).update(
              process_status = inputs['status']  
            )

            #get all sub-task
            subTask = Tasks.objects.filter(parent_id=task.id)

            if(subTask):
                for row in subTask:
                   UserTaskStatus.objects.create(
                       user_id = row.user_id,
                       task_id = row.id,
                       status = inputs['status'],
                       note = inputs['status'] if inputs['status'] else null,
                   )

    if(user.isQa or user.isTlQa):

        if((inputs['status'],'qc_rejected','completed')):
            Tasks.objects.filter(parent_id=task.id).update(
            process_status = inputs['status'])
            
            #update sub task
            Tasks.objects.filter(parent_id=task.id).update(
            process_status = inputs['status']  
            )

            #get all sub-task
            subTask = Tasks.objects.filter(parent_id=task.id)
            if(subTask):
                for row in subTask:
                    UserTaskStatus.objects.create(
                        user_id = row.user_id,
                        task_id = row.id,
                        status = inputs['status'],
                        note = inputs['status'] if inputs['status'] else null,
                    )

    return JsonResponse({'data':UserTaskStatusData},status=200)    
