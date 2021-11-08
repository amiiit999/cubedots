from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        
        if group == 'user' or request.user.role == 'user':
            return redirect('user_dashboard_index')
        if group == 'tl' or request.user.role == 'tl':
            return redirect('moni_task')  
        if group == 'qc' or request.user.role == 'qc':
                return redirect('moni_task')
        if group == 'TlQa' or request.user.role == 'TlQa':
            return redirect('moni_task')
        if group == 'qa' or request.user.role == 'qa':
            return redirect('moni_task') 
        if group == 'HR' or request.user.role == 'hr' or request.user.role == 'hr_admin':
            return redirect('hr_index') 

        if group == 'admin' or group == 'administrator' or request.user.role == 'admin' or request.user.role == 'administrator':
            return view_func(request, *args, **kwargs)
        if not group or request.user.role =='':
            return redirect('user_page')
        if group != '':
            return view_func(request, *args, **kwargs)    
    return wrapper_function
