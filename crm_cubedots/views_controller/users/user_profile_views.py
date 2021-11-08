from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from django.contrib.auth.models import Group 

from crm_cubedots.model.account import Account
from crm_cubedots.model.forms.accounts_forms import AccountsProfilePicForm,AccountResetPasswordForm

def userpage(request):
    context = {}
    return render(request,'users/dashboard/index.html',context)

def user_profile(request,id):
    Context = {}
    if request.method == "POST":
        update = Account.objects.get(id=id)
        form = AccountsProfilePicForm(request.POST,request.FILES, instance=update)
        if form.is_valid():
                form.save()
                messages.success(request, 'Profile Picture Updated Successfully !! ')
                return render(request, 'users/dashboard/profile.html',{'form':form})
        else:    
            Context['form'] = form
        return render(request, 'users/dashboard/profile.html', Context)
    else:
        update = Account.objects.get(id=id)
        form = AccountsProfilePicForm(instance=update)
        Context['form'] =form
        return render(request, 'users/dashboard/profile.html', Context) 

def user_profile_reset_password(request,id):
    user = request.user
    
    update = Account.objects.get(id=id)
    context = {}
    form = AccountResetPasswordForm(request.POST or None, instance=update)
    if form.is_valid():
            form.save()
            messages.success(request, 'Password Reset Successfully !! ')
            return redirect('user_dashboard_index')
    else:    
        context['form'] = form 
        return render(request, 'users/dashboard/reset_password.html',context)       