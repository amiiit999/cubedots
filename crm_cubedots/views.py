from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, admin_only
from django import template
from django.contrib.auth.models import Group 

from crm_cubedots.forms import AccountAuthenticationForm

register = template.Library() 

@register.filter(name='is_group') 
def is_group(user, group_name):
    group =  Group.objects.get(name=group_name) 
    return group in user.groups.all() 
# Create your views here.


def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():          
            fm.save()
            messages.success(request,"Registered Successfully !!")
            return redirect('/signin')
    else:
        fm = SignUpForm()        
    return render(request, 'auth/signup.html',{'form':fm})


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request=request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        fm = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': fm})

'''
@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        fm = AccountAuthenticationForm (data=request.POST)
        if fm.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        fm = AccountAuthenticationForm ()
    return render(request, 'auth/login.html', {'form': fm})
'''

def admin_dashboard(request):
    return render(request, 'admin/dashboard/index.html')


def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successfully !!")
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    context = {}
    return redirect('admin_dashboard_index')

