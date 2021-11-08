from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import template
from django.contrib.auth.models import Group 
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from crm_cubedots.model.account import Account
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def hr_emlpoyees_attendence_index(request):
    context = {}

    objects_data = Account.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,5) # Show 10 contacts per page.

    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request, 'hrs/attendence/index.html',context)