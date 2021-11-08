from django.template import context
from crm_cubedots.model.departments import Departments
from crm_cubedots.model.task import Tasks
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound,Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import serializers
from django.core.serializers import serialize
import datetime
from json import dumps
from collections import OrderedDict
from django.core.exceptions import PermissionDenied
from humanfriendly import format_timespan
from django.db.models import Avg, Count, Min, Sum, Max
from itertools import chain


from crm_cubedots.model.projects import Projects
from crm_cubedots.model.departments import Departments
from crm_cubedots.serializers import TaskSerializer
from crm_cubedots.model.task import Tasks
from crm_cubedots.model.account import Account
from crm_cubedots.model.user_task_logs import UserTaskLog
from crm_cubedots.model.user_task_status import UserTaskStatus

#---constants----
from crm_cubedots.constants import constants
def user_tasks(request):
    user = request.user
    id_list = Tasks.objects.filter(user_id = user.id, status = 'active').order_by('project_id').values_list('project_id',flat=True).exclude(process_status='completed').distinct()  
   
    objects_data = Projects.objects.filter(id__in=id_list,status='active').order_by('created_at').exclude(status='completed')

    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
   
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'users/tasks/index.html',{'page_obj': page_obj})

def user_tasks_search(request):
    context = {}
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        try:
            # user = request.user
            # id_list = Tasks.objects.filter(user_id = user.id, status = 'active').order_by('project_id').exclude(process_status = 'completed').values_list('project_id').distinct()  
            
            context['page_obj'] = Projects.objects.filter(Q(name__icontains=query) | Q(status__icontains=query), deleted_at=None)
            return render(request,'users/tasks/index.html', context)
        except:
                pass
    else:
        return redirect("user_tasks")


def user_tasks_showProjects(request,id):
    context = {}
    taskStatusTimerViewAccess = {}
    user = request.user

    if(user.isTl):
        taskStatusTimerViewAccess = constants.tl_as_user_task_process_status_timer_view_access
    elif(user.isQa or user.isTlQa):
        taskStatusTimerViewAccess = constants.qa_as_user_task_process_status_timer_view_access
    elif(user.isUser):
         taskStatusTimerViewAccess = constants.user_task_process_status_timer_view_access  
    else:
        return HttpResponseNotFound("This user role does not have access permission.")             

    project = Projects.objects.get(id=id)

    if (not project):
        raise PermissionDenied

    if (project.status != 'active'):
        raise PermissionDenied

    taskQuery = Tasks.objects.filter(status='active',parent_id=0,user_id=user.id,project_id=id,deleted_at=None)

    context['totalTasksStatics'] = taskQuery.count()

    context['tasksStaticsAssigned'] = taskQuery.filter(process_status="assigned").aggregate(assigned = Count("process_status"))

    context['tasksStaticsTlRejected'] = taskQuery.filter(process_status="tl_rejected").aggregate(tl_rejected = Count("process_status"))

    context['tasksStaticsQaRejected'] = taskQuery.filter(process_status="qc_rejected").aggregate(qa_rejected = Count("process_status"))

    context['tasksStaticsCompleted'] = taskQuery.filter(process_status="completed").aggregate(completed = Count("process_status"))

    if(user.isTl):
        context['tasksStatics'] = taskQuery.filter(process_status="tl_started").aggregate(started = Count("process_status"))
    elif(user.isUser):
        context['tasksStatics'] = taskQuery.filter(process_status="user_started").aggregate(started = Count("process_status"))
    elif(user.isQa):
        context['tasksStatics'] = taskQuery.filter(process_status="qc_started").aggregate(started = Count("process_status"))
    elif(user.isHr):
        context['tasksStatics'] = taskQuery.filter(process_status="user_started").aggregate(started = Count("process_status"))                
    else:
        return HttpResponseNotFound("This user role does not have access permission.")        

    context['project'] = Projects.objects.get(id=id)
    

    objects_data = Tasks.objects.filter(project_id=id,user_id = user.id,parent_id = 0,deleted_at=None).order_by('-created_at').exclude(process_status="completed")
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.

    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)

    return render(request,'users/tasks/showProjects.html',context)

def user_tasks_showProjects_search(request,id):
    context = {}
    user = request.user
    context['project'] = Projects.objects.get(id=id)
    project = Projects.objects.get(id=id)

    if (not project):
        raise PermissionDenied

    if (project.status != 'active'):
        raise PermissionDenied

    taskQuery = Tasks.objects.filter(status='active',parent_id=0,user_id=user.id,project_id=id)

    context['totalTasksStatics'] = taskQuery.count()

    context['tasksStaticsAssigned'] = taskQuery.filter(process_status="assigned").aggregate(assigned = Count("process_status"))

    context['tasksStaticsTlRejected'] = taskQuery.filter(process_status="tl_rejected").aggregate(tl_rejected = Count("process_status"))

    context['tasksStaticsQaRejected'] = taskQuery.filter(process_status="qc_rejected").aggregate(qa_rejected = Count("process_status"))

    context['tasksStaticsCompleted'] = taskQuery.filter(process_status="completed").aggregate(completed = Count("process_status"))

    if(user.isTl):
        context['tasksStatics'] = taskQuery.filter(process_status="tl_started").aggregate(started = Count("process_status"))
    elif(user.isUser):
        context['tasksStatics'] = taskQuery.filter(process_status="user_started").aggregate(started = Count("process_status"))
    elif(user.isQa):
        context['tasksStatics'] = taskQuery.filter(process_status="qc_started").aggregate(started = Count("process_status"))
    elif(user.isHr):
        context['tasksStatics'] = taskQuery.filter(process_status="user_started").aggregate(started = Count("process_status"))                
    else:
        return HttpResponseNotFound("This user role does not have access permission.")  

    if request.method == 'GET': # this will be GET now      
            query =  request.GET.get('search') # do some research what it does       
            try:
               
                context['page_obj'] = Tasks.objects.filter(Q(taskid__icontains=query) | Q(name__icontains=query) | Q(status__icontains=query),user_id = user.id , project_id = id, deleted_at=None,status = 'active', parent_id = 0)
                return render(request,'users/tasks/showProjects.html', context)
            except:
                    pass
    else:
        return redirect("user_tasks")   

def user_tasks_show(request,id):
    context = {}
    taskStatusListAccess = []
    
    user = request.user

    task = Tasks.objects.get(id=id)
    
    task_data = serializers.serialize("json",[Tasks.objects.get(id=id)])
    
    taskPrevious = Tasks.objects.filter(parent_id=task.parent_id , user_id = user.id, project_id = task.project_id, id__lt = task.id).order_by('-id').first()

    taskNext = Tasks.objects.filter(parent_id=task.parent_id , user_id = user.id, project_id = task.project_id, id__gt = task.id).order_by('id').first()

    todayDate=datetime.datetime.now().strftime("%Y-%m-%d")
    
    project = Projects.objects.filter(id=task.project_id).first()

    if(not project):

        return HttpResponseNotFound('<br /><h2>Task project not found.</h2>') 

    if(project.status != 'active'):
        raise PermissionDenied
    

    if(task.user_id == user.id and task.tl_id == user.id and task.qc_id == user.id and user.isTl):
        taskStatusListAccess =  [
            {'tl_started' : "start"},
            {'completed' : "completed"}
        ]
        taskStatusTimerViewAccess = [
            'assigned',
            'tl_started'
        ]
        # for tl (tl tl qc)
    elif(task.user_id == user.id and task.tl_id == user.id and task.qc_id != user.id and user.isTl):
        taskStatusListAccess =  [
           { 'tl_started' : "start"},
            {'forwarded_to_qc' : "submit"},
        ]

        taskStatusTimerViewAccess =  [
                'assigned',
                'tl_started',
                'qc_rejected',
            ]
        #for qc (qc qc qc)
    elif(task.user_id == user.id and (task.tl_id == task.qc_id) and user.isQa ):
        taskStatusListAccess = [
            {'qc_started' : "start"},        
            {'completed' : "completed"}
        ]
        taskStatusTimerViewAccess = [
           'assigned',
            'qc_started' 
        ]

        #for user (user qc qc)
    elif(task.user_id == user.id and (task.tl_id == task.qc_id) and user.isUser):    
        taskStatusListAccess = [{'user_started' : "start"},{'forwarded_to_qc' : "submit"}]
        taskStatusTimerViewAccess =  [
                'assigned',
                'user_started',
                'qc_rejected',
            ]
    else: 
        #forward to tl (user tl qc)
        taskStatusListAccess = [{'user_started' : "start"},{'forwarded_to_tl' : "submit"}]
        taskStatusTimerViewAccess =  [
                'assigned',
                'user_started',
                'tl_rejected',
                'qc_rejected',
            ]
   

    taskStatusListAccessData = json.dumps(taskStatusListAccess)
    taskStatusTimerViewAccessData = json.dumps(taskStatusTimerViewAccess)

    context = {'task_data': task_data,'task':task, 'taskPrevious':taskPrevious, 'taskNext':taskNext, 'todayDate':todayDate, 'taskStatusListAccessData':taskStatusListAccessData,'taskStatusTimerViewAccessData':taskStatusTimerViewAccessData }

    return render(request,'users/tasks/show.html',context)  

@api_view(['GET'])    
def user_task_api(request,id):
    tasks = Tasks.objects.get(id=id)
    serializer = TaskSerializer(tasks, many=False)
    return Response(serializer.data)   

def user_task_store_time(request,id):
    userTaskLogData = []
    taskStatus = []
    userTaskLog= []
    processStatus = []
    user = request.user
    task = Tasks.objects.get(id=id)
    
    if(task.user_id != user.id ):
        return JsonResponse({'error':'Unauthorized access'}, status_code=401)

    taskProcessStatusList = constants.USER_TASK_PROCESS_STATUS
    nowStartTime = datetime.datetime.now()
    
    if(user.isTl):
            processStatus =  taskProcessStatusList['tl_started']
    elif(user.isQa or user.isTlQa):
            processStatus =  taskProcessStatusList['qc_started']
    else:
        processStatus =  taskProcessStatusList['user_started']

   
    if(not task.work_started_at):
           
            Tasks.objects.filter(id = task.id).update(
            work_started_at =  nowStartTime,
            process_status = processStatus,
            )
    else:
        Tasks.objects.filter(id = task.id).update(
            process_status = processStatus,
            ) 

    # update task if start date is null and task is child mean belong to parent
        # update only for first time
    if(not task.work_started_at and task.parent_id > 0):
        Tasks.objects.filter(id = task.parent_id).update(
        work_started_at        = nowStartTime,
        process_status    = processStatus
        )
                
        # create task log
    userTaskLogData = UserTaskLog.objects.create(
        user_id         = user.id,
        task_id         = task.id,
         work_started_at = nowStartTime
    )
   
    userTaskLogDataSerialize = serializers.serialize("json", [userTaskLogData])
    userTaskLog = json.loads(userTaskLogDataSerialize)
    #     # create task status
    todayDate = nowStartTime.strftime("%m-%d-%Y")
    try:
        taskStatus = UserTaskStatus.objects.filter(user_id=user.id,task_id = task.id).latest('id')
    except:
        taskStatus = None
        

    statusData = {
        'user_id'   : user.id,
        'task_id'   : task.id,
        'status'    : processStatus  
    }
       
    if (taskStatus):
        if(taskStatus.status != statusData['status']):
            UserTaskStatus.objects.create(**statusData) 
    else:
        UserTaskStatus.objects.create(**statusData)
            
    return JsonResponse({'tasks':userTaskLog,'process_status':processStatus})

def get_ajax_task(request,id):
    user = request.user
    task = Tasks.objects.get(id=id)
    nowStartTime = datetime.datetime.now()
    todayDate = nowStartTime.strftime("%m-%d-%Y")
    
    taskData = Tasks.objects.filter(id=task.id,user_id=user.id).first()
    subTasksData = Tasks.objects.filter(parent_id=task.id,user_id=user.id).order_by('-id')
    
    taskDataSerialize = serializers.serialize("json", [taskData])
    tasks = json.loads(taskDataSerialize)
    
    subTaskDataSerialize = serializers.serialize("json", subTasksData)
    subtasks = json.loads(subTaskDataSerialize)

    

    return JsonResponse({'task':tasks,'subTask':subtasks,'todayDate':todayDate})

def get_ajax_task_log(request,id):
    user = request.user
    nowStartTime = datetime.datetime.now()
    task = Tasks.objects.get(id=id)

    todaydurations = UserTaskLog.objects.filter(user_id=user.id, task_id=task.id, created_at__date=nowStartTime.strftime("%Y-%m-%d")).aggregate(Sum('work_duration'))
    taskLogs = UserTaskLog.objects.filter(task_id = task.id,user_id=user.id).order_by('-created_at')
    taskLogsSerialize = serializers.serialize("json", taskLogs)
    tasks = json.loads(taskLogsSerialize)

    todayduration = todaydurations['work_duration__sum']
    
    return JsonResponse({'task':tasks,'todayduration':todayduration})

def get_ajax_task_status(request,id):
    
    user = request.user
    user_data = Account.objects.all()
    nowStartTime = datetime.datetime.now()
    task = Tasks.objects.get(id=id)
    taskStatusQuery = list(UserTaskStatus.objects.filter(task_id=task.id).values().order_by('-created_at'))
    # taskStatusSerialize = serializers.serialize("json", taskStatusQuery)
    # taskStatus = json.loads(taskStatusSerialize)
    #taskStatusQuery = list(UserTaskStatus.objects.filter(task_id=task.id).values())
    return JsonResponse({'taskStatus':taskStatusQuery},safe=False)

def ajax_update_status(request,id):
    inputs = []
   
    data = json.loads(request.body)
    user = request.user
    task = Tasks.objects.get(id=id)

    if(task.user_id != user.id):
        return JsonResponse({'error':'Unauthorized access'}, status_code=401)
    inputs = data

    inputs['user_id'] = user.id
    inputs['task_id'] = task.id
    

    userTaskStatusData = UserTaskStatus.objects.create(**inputs)

  
    Tasks.objects.filter(id=task.id).update(
        process_status = inputs['status']
    )

    userTaskStatusSerializer = serializers.serialize("json", [userTaskStatusData])
    userTaskStatus = json.loads(userTaskStatusSerializer)
    
    if(task.parent_id > 0 and (inputs['status'],'forwarded_to_tl','forwarded_to_qc','completed')):
        subTask = Tasks.objects.filter(parent_id=task.parent_id)
        totalSubTaskCounts = subTask.count()
        workedSubTaskCounts = subTask.filter(process_status = inputs['status']).count()
       
        if(totalSubTaskCounts == workedSubTaskCounts):
            Tasks.objects.filter(id=task.parent_id).update(process_status=inputs['status'])

    return JsonResponse({'data':userTaskStatus},status=200)

def update_time(request,id):
    totalAmonut = []
    date_format = "%Y-%m-%d %H:%M:%S.%f"

    user = request.user
    task = Tasks.objects.get(id=id)

    if(task.user_id != user.id):
        return JsonResponse({'error':'Unauthorized access'}, status_code=401)

    taskFinishTime = datetime.datetime.now();
    taskLogFinishTime = datetime.datetime.now();
    
    userTaskLogQuery = UserTaskLog.objects.filter(user_id=user.id,task_id=task.id,work_started_at__date=taskLogFinishTime.strftime("%Y-%m-%d")).order_by('-created_at').first()
    userTaskLogSerialize = serializers.serialize("json", [userTaskLogQuery])
    userTaskLog = json.loads(userTaskLogSerialize)

    
    if(userTaskLogQuery):
        taskLogStartTime = userTaskLogQuery.work_started_at

        time_start = str(taskLogStartTime)
        time_end = str(taskLogFinishTime)
        
        diff = datetime.datetime.strptime(time_end, date_format) - datetime.datetime.strptime(time_start, date_format)
        diff_minutes = diff.total_seconds() // 60

        #update task log
        UserTaskLog.objects.filter(id=userTaskLogQuery.id).update(
            work_ended_at = taskLogFinishTime,
            work_duration = diff_minutes
        )

        totalDurationQuery = UserTaskLog.objects.filter(user_id=user.id,task_id=task.id).aggregate(Sum('work_duration'))
        
        #time = format_timespan(diff_hours)
        
        Tasks.objects.filter(id=task.id).update(
            work_ended_at = taskFinishTime,
            work_duration = totalDurationQuery['work_duration__sum']
        )
       
        if(task.parent_id):
            fromChildTask = Tasks.objects.filter(user_id=user.id,parent_id=task.parent_id).aggregate(Min("work_started_at"), Max("work_ended_at"),Sum("work_duration"))
          
            if(fromChildTask):
                    Tasks.objects.filter(id=task.parent_id).update(
                        work_started_at         = fromChildTask['work_started_at__min'],
                        work_ended_at           = fromChildTask['work_ended_at__max'],
                        work_duration           = fromChildTask['work_duration__sum']
                    );
                
        return JsonResponse({'data':userTaskLog},status=200)

