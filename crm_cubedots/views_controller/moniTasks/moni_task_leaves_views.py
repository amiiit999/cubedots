from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from crm_cubedots.model.apply_leaves import ApplyLeave
from crm_cubedots.model.manager import TeamLeader
from crm_cubedots.model.forms.managerApproveLeaves_forms import ApproveLeavesForm
from crm_cubedots.model.forms.applyLeaves_forms import ApplyLeavesForm
from crm_cubedots.model.manager import Manager
from crm_cubedots.model.manager import TeamLeader
from crm_cubedots.model.account import Account

def leaves_index(request):
    context = {}
    user = request.user
    try:
        if(user.role == 'tl'):
            context['total_emp_leaves'] = ApplyLeave.objects.filter(deleted_at=None,tl_id = user.id).exclude(user_id=user.id).count()
            
            context['total_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id = user.id).count()
            context['approved_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id,approval_status='approved').count()
            context['pending_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id,approval_status='pending').count()
            context['rejected_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id,approval_status='rejected').count()
        
        if(user.role == 'qa'):
            context['total_emp_leaves'] = ApplyLeave.objects.filter(deleted_at=None,manager_id = user.id).count()
            context['total_tl_leaves'] = ApplyLeave.objects.filter(deleted_at=None,tl_id = user.id).count()
            
            
            context['total_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id = user.id).count()
            context['approved_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id,approval_status='approved').count()
            context['pending_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id,approval_status='pending').count()
            context['rejected_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id,approval_status='rejected').count()     
    except:
        pass
    return render(request, 'moni_task/leaves/index.html',context)

def approve_leaves_index(request):
    context = {}
    user = request.user 
    if(user.role == 'tl'):
        objects_data = ApplyLeave.objects.filter(deleted_at = None,tl_id = user.id).exclude(user_id=user.id).order_by('-updated_at')    
       
    if(user.role == 'qa'):
        user_role_id = Account.objects.filter(deleted_at=None,role='tl').values_list('id',flat=True).order_by('id')
        
        objects_data = ApplyLeave.objects.filter(deleted_at = None,manager_id = user.id).exclude(user_id=user.id).order_by('-updated_at')
    # objects_data = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id).order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
   
    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request, 'moni_task/leaves/leaves_approval/index.html',context)

def approve_leaves_update(request,id):
    context = {}
    update = ApplyLeave.objects.get(id=id)
    user = request.user
    form = ApproveLeavesForm(request.POST or None, instance=update)
    if form.is_valid():
        try:
            instance = form.save(commit=False)
            instance.approval_status    = request.POST['approval_status']
            if(user.role == 'tl'):
                instance.tl_approval        = request.POST['approval_status']
                instance.manager_approval        = 'pending'
            
            if(user.role == 'qa'): 
                if (update.tl_approval):
                    instance.tl_approval        = update.tl_approval if update.tl_approval else 'pending'
                    instance.manager_approval        = request.POST['approval_status']
                else:
                    instance.manager_approval        = request.POST['approval_status']  
            form.save()
            messages.success(request, 'Approval Updated Successfully !! ')
            return redirect("approve_leaves_index")
        except:
            pass
    else:    
        context['form'] = form
    return render(request, 'moni_task/leaves/leaves_approval/edit.html', context) 

def approve_leaves_show(request,id):
    context = {}

    context['data'] = ApplyLeave.objects.get(id=id)
    return render(request, 'moni_task/leaves/leaves_approval/show.html',context)

def apply_leaves_index(request):
    context = {}
    user = request.user
    
    objects_data = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id).order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
   
    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request,'moni_task/leaves/apply_leaves/index.html',context)

def apply_leaves_create(request):
    context = {}
    context['form'] = ApplyLeavesForm()

    return render(request, 'moni_task/leaves/apply_leaves/create.html',context)

def apply_leaves_store(request):
    user = request.user
    date_format = "%Y-%m-%d"
    team_leader = []
    manager = []
    try:
        team_leader = TeamLeader.objects.filter(user_id = user.id).order_by('-created_at').first()       
        manager     = Manager.objects.filter(user_id = user.id).order_by('-created_at').first()
        
    except:
        pass
    
    if request.method == "POST":
           
        form = ApplyLeavesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.leaves_type_id     = request.POST['leaves_type']
            instance.approval_status    = 'pending'
            if(user.role == 'tl'):
                instance.manager_approval   = 'pending'    
            instance.department_id      = user.department_id
            instance.user_id            = user.id
            if(team_leader or manager):
                instance.tl_id              = team_leader.tl_id
                instance.manager_id         = manager.manager_id
            else:
                messages.error(request, 'Contact HR to Allot Manager & TL') 
                return redirect("moni_tasks_apply_leaves_index")
            instance.start_date         = request.POST['start_date']
            instance.end_date           = request.POST['end_date']

            date_from = datetime.strptime(str(request.POST['end_date']),date_format)
            date_to = datetime.strptime(str(request.POST['start_date']),date_format)
            total = date_from-date_to

            instance.total  = total.days +1
            instance.save()
            messages.success(request, 'Leaves Applied Successfully !! ')
            return redirect("moni_tasks_apply_leaves_index")
        else:  
            return render(request, 'moni_task/leaves/apply_leaves/create.html', {'form': form}) 

def apply_leaves_update(request,id):
    user = request.user
    context = {}
    date_format = "%Y-%m-%d"
    update = ApplyLeave.objects.get(id=id)

    form = ApplyLeavesForm(request.POST or None, instance=update)
    if form.is_valid():
        try:
            instance = form.save(commit=False)
            
            if(user.role == 'tl'):
                instance.approval_status    = 'pending'
                instance.start_date         = request.POST['start_date']
                instance.end_date           = request.POST['end_date']

                date_from = datetime.strptime(str(request.POST['end_date']),date_format)
                date_to = datetime.strptime(str(request.POST['start_date']),date_format)
                total = date_from - date_to

                instance.total  = total.days +1
               

            instance.save()
            messages.success(request, 'Leave Updated Successfully !! ')
            return redirect("moni_tasks_apply_leaves_index")
        except:
            pass
    else:    
        context['form'] = form
    return render(request, 'moni_task/leaves/apply_leaves/edit.html', context)             

def apply_leaves_show(request,id):
    context = {}
    context['data']  = ApplyLeave.objects.get(id=id)
    return render(request, 'moni_task/leaves/apply_leaves/show.html', context)