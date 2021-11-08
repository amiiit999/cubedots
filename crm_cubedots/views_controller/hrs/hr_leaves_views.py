from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crm_cubedots.model.forms.hr_leave_types_form import LeaveTypesForm
from crm_cubedots.model.leaves_type import LeaveTypes
from crm_cubedots.model.apply_leaves import ApplyLeave
from crm_cubedots.model.account import Account
from crm_cubedots.model.forms.applyLeaves_forms import ApplyLeavesForm
from crm_cubedots.model.forms.managerApproveLeaves_forms import ApproveLeavesForm

def hrAdmin_leaves_index(request):
    context = {}
    user = request.user

    manager_role_id = Account.objects.filter(role='qa').values_list('id',flat=True).order_by('created_at')
    context['total_manager_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = manager_role_id).order_by('-created_at').count()

    employee_role_id = Account.objects.filter(role='user').values_list('id',flat=True).order_by('created_at')
    context['total_emp_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = employee_role_id).order_by('-created_at').count()
    context['total_emp_leaves_approved'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = employee_role_id,approval_status='approved').order_by('-created_at').count()
    context['total_emp_leaves_pending'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = employee_role_id,approval_status='pending').order_by('-created_at').count()
    context['total_emp_leaves_rejected'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = employee_role_id,approval_status='rejected').order_by('-created_at').count()

    tl_role_id = Account.objects.filter(role='tl').values_list('id',flat=True).order_by('created_at')
    context['total_tl_leaves'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = tl_role_id).order_by('-created_at').count()
    context['total_tl_leaves_approved'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = tl_role_id,approval_status='approved').order_by('-created_at').count()
    context['total_tl_leaves_pending'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = tl_role_id,approval_status='pending').order_by('-created_at').count()
    context['total_tl_leaves_rejected'] = ApplyLeave.objects.filter(deleted_at=None,user_id__in = tl_role_id,approval_status='rejected').order_by('-created_at').count()

    
    
    return render(request, 'hrs/leaves/index.html',context)

def hrAdmin_leaves_approval_index(request):
    context = {}
    user = request.user
    manager_role_id = Account.objects.filter(deleted_at=None,role='qa').values_list('id',flat=True).order_by('created_at')
    
    objects_data = ApplyLeave.objects.filter(deleted_at=None,user_id__in = manager_role_id).order_by('-updated_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
    
    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request, 'hrs/leaves/approve_leaves/managers/index.html',context)  

def hrAdmin_leaves_approval_update(request,id):
    context = {}
    update = ApplyLeave.objects.get(id=id)
    user = request.user
    form = ApproveLeavesForm(request.POST or None, instance=update)
    if form.is_valid():
        try:
            instance = form.save(commit=False)
            instance.approval_status    = request.POST['approval_status']
            form.save()
            messages.success(request, 'Approval Updated Successfully !! ')
            return redirect("hrAdmin_leaves_approval_index")
        except:
            pass
    else:    
        context['form'] = form
    return render(request, 'hrs/leaves/approve_leaves/managers/edit.html', context)       

def hrAdmin_leaves_approval_show(request,id):
    context =  {}

    context['data'] = ApplyLeave.objects.get(id=id)

    return render(request, 'hrs/leaves/approve_leaves/managers/show.html', context)    

def tl_leaves_approval_index(request):
    context = {}
    user = request.user
    tl_role_id = Account.objects.filter(deleted_at = None,role='tl').values_list('id',flat=True).order_by('created_at')
    
    objects_data = ApplyLeave.objects.filter(deleted_at=None,user_id__in = tl_role_id).order_by('-updated_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
    
    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request, 'hrs/leaves/approve_leaves/team_leaders/index.html', context)

def tl_leaves_approval_show(request,id):
    context = {}
    
    context['data'] = ApplyLeave.objects.get(id=id)

    return render(request, 'hrs/leaves/approve_leaves/team_leaders/show.html',context)

def users_leaves_approval_index(request):
    context = {}
    user = request.user
    user_role_id = Account.objects.filter(deleted_at = None,role='user').values_list('id',flat=True).order_by('created_at')
    
    objects_data = ApplyLeave.objects.filter(deleted_at=None,user_id__in = user_role_id).order_by('-updated_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.
    
    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request, 'hrs/leaves/approve_leaves/employees/index.html', context)

def users_leaves_approval_show(request,id):    
    context = {}
    context['data'] = ApplyLeave.objects.get(id=id)

    return render(request, 'hrs/leaves/approve_leaves/employees/show.html',context)