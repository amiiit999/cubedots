from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.contrib import messages
from django import template
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from crm_cubedots.decorators import unauthenticated_user, admin_only


from crm_cubedots.model.account import Account
from crm_cubedots.model.forms.accounts_forms import AccountsForm , AccountShortForm , AccountsProfilePicForm, AccountResetPasswordForm
from crm_cubedots.model.manager import Manager
from crm_cubedots.model.manager import TeamLeader




@login_required(login_url='login')
def users_index(request):
    objects_data = Account.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'admin/users/index.html',{'page_obj': page_obj}) 

@login_required(login_url='login')

def users_create(request):
    Context = {}
    Context['form'] = AccountShortForm()
    return render(request,'admin/users/create.html',Context)  

@login_required(login_url='login')

def users_store(request):
    if request.method == "POST":
        
        form = AccountShortForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.approval_status = 'pending'
            instance.save()
            messages.success(request, 'User Added Successfully !! ')
            return redirect("admin_user_index")
        else:  
            return render(request, 'admin/users/create.html', {'form': form})     
@login_required(login_url='login')

def users_update(request,id):
    Context = {}
    user = Account.objects.get(id=id)
    
    form = AccountsForm(request.POST or None, instance=user)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            manager = Account.objects.get(id = request.POST['manager_name'])
            team_leader = Account.objects.get(id = request.POST['team_leader'])
           
            Manager.objects.update_or_create(name=manager.first_name+' '+manager.last_name,user_id=user.id,manager_id = request.POST['manager_name'])
            TeamLeader.objects.update_or_create(name=team_leader.first_name+' '+team_leader.last_name,user_id=user.id,tl_id =request.POST['team_leader'] )        
            
            messages.success(request, 'User Updated Successfully !! ')
            return redirect("admin_user_index")
    else:    
        Context['form'] = form
    return render(request, 'admin/users/edit.html', Context)          

@login_required(login_url='login')

def users_soft_delete(request,id):
    Account.objects.get(id=id).soft_delete()
    messages.success(request, 'User Deleted Successfully !! ')
    return redirect('admin_user_index')

@login_required(login_url='login')

def users_search(request):
    context = {}
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        try:
            context['page_obj'] = Account.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(email__icontains=query) | Q(approval_status__icontains=query),  deleted_at=None)
            return render(request,'admin/users/index.html', context)
        except:
                pass
    else:
        return redirect("admin_user_index")     
@login_required(login_url='login')


def users_profile_pic(request,id):
   
    Context = {}
    if request.method == "POST":
        update = Account.objects.get(id=id)
        
        form = AccountsProfilePicForm(request.POST or None,request.FILES, instance=update)
        if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.success(request, 'Profile Picture Updated Successfully !! ')
                return render(request, 'admin/users/profile.html',{'form':form})
        else:    
            Context['form'] = form
        return render(request, 'admin/users/profile.html', Context)
    else:
        update = Account.objects.get(id=id)
        form = AccountsProfilePicForm(instance=update)
        Context['form'] =form
        return render(request, 'admin/users/profile.html', Context)      
login_required(login_url='login')
def reset_password(request,id):
    update = Account.objects.get(id=id)
    Context = {}
    form = AccountResetPasswordForm(request.POST or None, instance=update)
    if form.is_valid():
            form.save()
            messages.success(request, 'Password Reset Successfully !! ')
            return redirect('admin_user_index')
    else:    
        Context['form'] = form
    return render(request, 'admin/users/reset_password.html', Context)