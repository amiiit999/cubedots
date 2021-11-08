from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crm_cubedots.model.forms.hr_leave_types_form import LeaveTypesForm
from crm_cubedots.model.leaves_type import LeaveTypes


def create(request):
    context = {}
    context['form'] = LeaveTypesForm()

    return render(request, 'hrs/leave_types/create.html',context)

def store(request):
    if request.method == "POST":
        
        form = LeaveTypesForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Leave Added Successfully !! ')
                return redirect("hr_leaves_type_index")
            except:
                pass
        else:
            return render(request, 'hrs/leave_types/create.html', {'form': form})   

def index(request):
    context = {}

    objects_data = LeaveTypes.objects.filter(deleted_at=None)
    page = request.GET.get('page', 1)
    paginator = Paginator(objects_data,10) # Show 10 contacts per page.

    try:
        context['page_obj'] = paginator.page(page)
    except PageNotAnInteger:
        context['page_obj'] = paginator.page(1)
    except EmptyPage:
        context['page_obj'] = paginator.page(paginator.num_pages)
    return render(request, 'hrs/leave_types/index.html',context)

def update(request,id):

    context = {}
    update = LeaveTypes.objects.get(id=id)

    form = LeaveTypesForm(request.POST or None, instance=update)
    if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Leave Type Updated Successfully !! ')
            return redirect("hr_leaves_type_index")
        except:
            pass
    else:    
        context['form'] = form
    return render(request, 'hrs/leave_types/edit.html', context) 

def soft_delete(request,id):
    destroy = LeaveTypes.objects.get(id=id)
    destroy.soft_delete()

    messages.success(request, "Leave Type Deleted Successfully")
    return redirect('hr_leaves_type_index')    