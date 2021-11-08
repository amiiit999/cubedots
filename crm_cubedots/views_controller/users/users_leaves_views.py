from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.contrib import messages
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

from crm_cubedots.model.forms.applyLeaves_forms import ApplyLeavesForm
from crm_cubedots.model.leaves_type import LeaveTypes
from crm_cubedots.model.apply_leaves import ApplyLeave
from crm_cubedots.model.manager import Manager
from crm_cubedots.model.manager import TeamLeader

def emp_leaves_dashboard(request):
    context = {}
    user = request.user
    try:
        if(user.role == 'user'):
            context['total_apprd_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id = user.id,approval_status='approved').count()
            context['total_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id=user.id).count()
            context['total_pending_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id = user.id,approval_status='pending').count()
            context['total_rejected_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id = user.id,approval_status='rejected').count()

    except:
        pass
    return render(request, 'users/leaves/index.html',context)

def emp_leaves_index(request):
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
    return render(request,'users/leaves/apply_leaves/index.html',context)


def apply_leaves_create(request):
    context = {}
    context['form'] = ApplyLeavesForm()

    return render(request, 'users/leaves/apply_leaves/create.html',context)
def apply_leaves_store(request):
    user = request.user
    date_format = "%Y-%m-%d"
    team_leader = TeamLeader.objects.filter(user_id = user.id).order_by('-created_at').first()
    manager     = Manager.objects.filter(user_id = user.id).order_by('-created_at').first()
    if request.method == "POST":
            
        form = ApplyLeavesForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.leaves_type_id     = request.POST['leaves_type']
            instance.approval_status    = 'pending'
            instance.tl_approval        = 'pending'
            instance.manager_approval   = 'pending'
            instance.department_id      = user.department_id
            instance.user_id            = user.id
            instance.tl_id              = team_leader.tl_id
            instance.manager_id         = manager.manager_id
            instance.start_date         = request.POST['start_date']
            instance.end_date           = request.POST['end_date']

            date_from = datetime.strptime(str(request.POST['end_date']),date_format)
            date_to = datetime.strptime(str(request.POST['start_date']),date_format)
            total = date_from-date_to

            instance.total  = total.days +1
            instance.save()
            messages.success(request, 'Leaves Applied Successfully !! ')
            return redirect("user_dashboard_index")
        else:  
            return render(request, 'users/leaves/apply_leaves/create.html', {'form': form}) 

def emp_leaves_show(request,id):
    context = {}

    context['data'] = ApplyLeave.objects.get(id=id)
    return render(request,'users/leaves/apply_leaves/show.html',context)            

def emp_leaves_update(request,id):
    context = {}
    user = request.user
    update = ApplyLeave.objects.get(id=id)
    date_format = "%Y-%m-%d"
    form = ApplyLeavesForm(request.POST or None, instance=update)
    if form.is_valid():
        try:
            instance = form.save(commit=False)
            
            if(user.role == 'user'):
                instance.approval_status    = 'pending'
                instance.start_date         = request.POST['start_date']
                instance.end_date           = request.POST['end_date']

                date_from = datetime.strptime(str(request.POST['end_date']),date_format)
                date_to = datetime.strptime(str(request.POST['start_date']),date_format)
                total = date_from - date_to

                instance.total  = total.days +1
               

            instance.save()
            messages.success(request, 'Leave Updated Successfully !! ')
            return redirect("emp_leaves_index")
        except:
            pass
    else:    
        context['form'] = form
    return render(request, 'users/leaves/apply_leaves/edit.html', context) 