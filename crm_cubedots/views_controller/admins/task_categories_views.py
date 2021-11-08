from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.contrib import messages
from django import template

from crm_cubedots.model.task_categories import TaskCategories
from crm_cubedots.model.forms.task_categories_forms import TaskCategoriesForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from crm_cubedots.constants.constants import PARENT_ID

def taskCategories_create(request):
    form = TaskCategoriesForm()
    return render(request,'admin/taskCategories/create.html',{'form':form})

def taskCategories_index(request):
    objects_data = TaskCategories.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 25 contacts per page.

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'admin/taskCategories/index.html',{'page_obj': page_obj})

def taskCategories_store(request):
     if request.method == "POST":
        
        form = TaskCategoriesForm(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.parent_id = request.POST['parent_id']
                
                instance.save()   
                messages.success(request, 'Task Category Added Successfully !! ')
                return redirect("taskCategory_index")
            except:
                pass    
        else:
            messages.error(request, 'Failed')
        return redirect("taskCategory_create")

def taskCategories_search(request):
    context = {}
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        try:
            context['page_obj'] = TaskCategories.objects.filter(name__icontains=query, deleted_at=None)
            return render(request,'admin/taskCategories/index.html', context)
        except:
                pass
    else:
        return redirect("taskCategory_index")   

def taskCategories_show(request,id):
    Context = {}
    Context['row'] = TaskCategories.objects.get(id=id)
    return render(request,'admin/taskCategories/show.html',Context)

def taskCategories_update(request,id):
    update = TaskCategories.objects.get(id=id)
    Context = {}
    form = TaskCategoriesForm(request.POST or None, instance=update)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Task Category Updated Successfully !! ')
            return redirect("taskCategory_index")
        except:
            pass
    else:    
        Context['form'] = form
    return render(request, 'admin/taskCategories/edit.html', Context)      

def taskCategories_soft_delete(request,id):
    TaskCategories.objects.get(id=id).soft_delete()
    messages.success(request, 'Tasks Category Deleted Successfully !! ')
    return redirect('taskCategory_index')


            