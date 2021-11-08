from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from django.contrib.auth.models import Group 
from django.db.models import Q

from crm_cubedots.model.account import Account
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crm_cubedots.model.forms.accounts_forms import AccountsProfilePicForm, AccountsForm, AccountShortForm, AccountResetPasswordForm

from crm_cubedots.model.manager import Manager
from crm_cubedots.model.manager import TeamLeader

def hr_index(request):
    context = {}
    context['row'] = Account.objects.filter(deleted_at=None)
    context['total_emp'] = Account.objects.filter(deleted_at=None).count()
    return render(request,'hrs/dashboard/index.html',context)

def hr_employees_index(request):
    context = {}

    objects_data = Account.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,5) # Show 10 contacts per page.

    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request, 'hrs/employees/index.html',context)

def hr_employees_search(request):
    context = {}

    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        
        context['page_obj'] = Account.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(approval_status__icontains=query),deleted_at=None)
        return render(request,'hrs/employees/index.html', context)
        
    else:
        return redirect("admin_task_index")      

def hr_employee_profile(request,id):
    Context = {}
    if request.method == "POST":
        update = Account.objects.get(id=id)
        print("profile",update.id)
        form = AccountsProfilePicForm(request.POST or None,request.FILES, instance=update)
        if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Profile Picture Updated Successfully !! ')
                return render(request, 'hrs/employees/profile.html',{'form':form})
        else:    
            Context['form'] = form
        return render(request, 'hrs/employees/profile.html', Context)
    else:
        update = Account.objects.get(id=id)
        form = AccountsProfilePicForm(instance=update)
        Context['form'] =form
        return render(request, 'hrs/employees/profile.html', Context) 

def hr_employee_update(request,id):
    context = {}
    user = Account.objects.get(id=id)

    form = AccountsForm(request.POST or None, instance=user)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            manager = Account.objects.get(id = request.POST['manager_name'])
            team_leader = Account.objects.get(id = request.POST['team_leader'])
           
            Manager.objects.update_or_create(name=manager.first_name+' '+manager.last_name,user_id=user.id,manager_id = request.POST['manager_name'])
            TeamLeader.objects.update_or_create(name=team_leader.first_name+' '+team_leader.last_name,user_id=user.id,tl_id =request.POST['team_leader'] )        
            
            messages.success(request, 'Employee Updated Successfully !! ')
            return redirect("hr_employees")
    else:    
        context['form'] = form
    return render(request, 'hrs/employees/edit.html', context)  

def hr_employee_create(request):
    context = {}
    context['form'] = AccountShortForm()
    return render(request,'hrs/employees/create.html',context)  

def hr_employee_store(request):
    if request.method == "POST":
        
        form = AccountShortForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.approval_status = 'pending'
            instance.save()
            messages.success(request, 'Employee Added Successfully !! ')
            return redirect("hr_employees")
        else:
            # messages.error(request, 'Error Raised')  
            return render(request, 'hrs/employees/create.html', {'form': form})   

def hr_employee_soft_delete(request,id):
    Account.objects.get(id=id).soft_delete()
    messages.success(request, 'Employee Deleted Successfully !! ')
    return redirect('hr_employees')

def hr_employee_reset_password(request,id):
    update = Account.objects.get(id=id)
    context = {}
    form = AccountResetPasswordForm(request.POST or None, instance=update)
    if form.is_valid():
            form.save()
            messages.success(request, 'Password Reset Successfully !! ')
            return redirect('hr_employee_profile',id=id)
    else:    
        context['form'] = form
    return render(request, 'hrs/employees/reset_password.html',context)  

def hr_admin_index(request):
    context = {}

    context['hr_admin'] = Account.objects.filter(role__in=['hr_admin','hr'],deleted_at=None)
    
    return render(request, 'hrs/employees/hr_admin/index.html',context)  

