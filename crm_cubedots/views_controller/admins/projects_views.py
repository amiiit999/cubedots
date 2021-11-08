from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.contrib import messages
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crm_cubedots.model.projects import Projects
from crm_cubedots.model.forms.projects_forms import ProjectsForm


def project_create(request):
    Context = {}
    Context['form'] = ProjectsForm()
    return render(request,'admin/projects/create.html',Context)

def project_store(request):
    if request.method == "POST":
    
        form = ProjectsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Project Added Successfully !! ')
                return redirect("project_index")
            except:
                pass
        else:
            return render(request, 'admin/projects/create.html', {'form': form})

def project_index(request):
    objects_data = Projects.objects.filter(deleted_at=None).order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 25 contacts per page.

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(request,'admin/projects/index.html',{'page_obj': page_obj})   

def project_update(request,id):
        update = Projects.objects.get(id=id)
        context = {}
        form = ProjectsForm(request.POST or None, instance=update)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Project Updated Successfully !! ')
                return redirect("project_index")
            except:
                pass
        else:    
            context['form'] = form
        return render(request, 'admin/projects/edit.html', context) 

def project_soft_delete(request,id):
    destroy = Projects.objects.get(id=id)
    destroy.soft_delete()
    messages.success(request, 'Project Deleted Successfully !! ')
    return redirect("project_index")  

def project_show(request,id):
    Context = {}
    Context['row'] = Projects.objects.get(id=id)
    return render(request,'admin/projects/show.html',Context)  

def project_search(request):
    context = {}
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        try:
            context['page_obj'] = Projects.objects.filter(name__icontains=query, deleted_at=None)
            return render(request,'admin/projects/index.html', context)
        except:
                pass
    else:
        return redirect("project_index")          