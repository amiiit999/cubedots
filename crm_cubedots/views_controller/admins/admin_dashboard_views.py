from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import Template, Context
from django.contrib import messages
from django import template
from django.db.models import query
from django.core import serializers
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponse
import json

from crm_cubedots.model.projects import Projects
login_required(login_url='login')
def dashboard_index(request):
    context = {}
    context['projects_count'] = Projects.objects.all().count()
    context['active_projects_count'] = Projects.objects.filter(status='active').count()
    context['completed_projects_count'] = Projects.objects.filter(status='completed').count()
    context['onHold_projects_count'] = Projects.objects.filter(status='on-hold').count()
    context['upcoming_projects_count'] = Projects.objects.filter(status='upcoming').count()

    return render(request, 'admin/dashboard/index.html',context)
login_required(login_url='login')
def projectsCounts(request,status_type):

    response_data =  {}
    data = Projects.objects.filter(status=status_type)
    response_data = serializers.serialize('json', data)
    return HttpResponse(json.dumps({'response_data':response_data}), content_type='application/json')
