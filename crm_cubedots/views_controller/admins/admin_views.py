from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from crm_cubedots.model.forms.projects_categories_forms import ProjectsCategoriesForm
from django.contrib.auth.models import Group 

def create_project_categories(request):
    fm = ProjectsCategoriesForm()
  
    return render(request,'admin/projectsCategories/create.html',{'form':fm})