from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib import messages
from django.contrib.auth.models import Group
from django import template

from crm_cubedots.model.forms.projects_categories_forms import ProjectsCategoriesForm
from crm_cubedots.model.project_categories import ProjectsCategories
from django.core.paginator import Paginator



def project_categories_create(request):
    fm = ProjectsCategoriesForm()

    return render(request, 'admin/projectsCategories/create.html', {'form': fm})


def project_categories_store(request):
    if request.method == "POST":

        form = ProjectsCategoriesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Project Category Added Successfully !! ')
                return redirect("project_category_index")
            except:
                pass
        else:
            messages.error(request, 'Failed')
        return render(request, 'admin/projectsCategories/create.html', {'form': form})


def project_categories_show(request, id):
    context = {}
    context['row'] = ProjectsCategories.objects.get(id=id)
    return render(request, 'admin/projectsCategories/show.html', context)


def project_categories(request):
    objects_data = ProjectsCategories.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 25 contacts per page.

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'admin/projectsCategories/index.html',{'page_obj':page_obj})

'''
def project_categories_edit(request, id):
    category = ProjectsCategories.objects.get(id=id)
    context = {}
    context["form"] = ProjectsCategoriesForm(
        request.POST or None, instance=category)
    return render(request, 'admin/projectsCategories/edit.html', context)
'''

def project_categories_update(request, id):
    category = ProjectsCategories.objects.get(id=id)
    Context = {}
    form = ProjectsCategoriesForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, 'Project Category Updated Successfully !! ')
        return redirect("project_category_index")
    Context['form'] = form
    return render(request, 'admin/projectsCategories/edit.html', Context)


def project_categories_destroy(request, id):
    category = ProjectsCategories.objects.get(id=id)
    category.soft_delete()
    messages.success(request, 'Project Category Deleted Successfully !! ')
    return redirect("project_category_index")


def project_categories_search(request):  
    context = {}
    if request.method == 'GET': # this will be GET now      
        query =  request.GET.get('search') # do some research what it does       
        try:
            context['page_obj'] = ProjectsCategories.objects.filter(name__icontains=query,deleted_at=None)
            return render(request,'admin/projectsCategories/index.html', context)
        except:
                pass
    else:
        return redirect("project_category_index")