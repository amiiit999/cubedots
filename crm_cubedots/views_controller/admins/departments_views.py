from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.contrib import messages
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crm_cubedots.model.departments import Departments
from crm_cubedots.model.forms.departements_forms import DepartmentsForm

def departments_create(request):
    Context = {}
    Context['form'] = DepartmentsForm()
    return render(request,'admin/departments/create.html',Context)

def departments_store(request):
    if request.method == "POST":
        
        form = DepartmentsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Department Added Successfully !! ')
                return redirect("department_index")
            except:
                pass
        else:
            messages.error(request, 'Failed')
        return render(request, 'admin/projectsCategories/create.html', {'form': form}) 

def departments_index(request):
    objects_data = Departments.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'admin/departments/index.html',{'page_obj': page_obj})

def departments_update(request,id):
        update = Departments.objects.get(id=id)
        context = {}
        form = DepartmentsForm(request.POST or None, instance=update)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Department Updated Successfully !! ')
                return redirect("department_index")
            except:
                pass
        else:    
            context['form'] = form
        return render(request, 'admin/departments/edit.html', context)  
'''
def departments_edit(request,id):
    edit = Departments.objects.get(id=id)
    Context = {}
    Context['form'] =  DepartmentsForm(request.POST or None, instance=edit)
    return render(request,'admin/departments/edit.html',Context)
'''
def departments_soft_delete(request,id):
    destroy = Departments.objects.get(id=id)  
    destroy.soft_delete()
    messages.success(request, 'Department Deleted Successfully !! ')
    return redirect("department_index")    

def departments_search(request):
    context = {}
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        try:
            context['page_obj'] = Departments.objects.filter(name__icontains=query, deleted_at=None)
            return render(request,'admin/departments/index.html', context)
        except:
                pass
    else:
        return redirect("department_index")     \

def departments_show(request,id):
    Context = {}
    Context['row'] = Departments.objects.get(id=id)
    return render(request,'admin/departments/show.html',Context) 
                                