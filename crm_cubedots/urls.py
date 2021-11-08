"""crmCubedotsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from crm_cubedots import views

from crm_cubedots.views_controller.admins import admin_tasks_views
from crm_cubedots.views_controller.admins import admin_dashboard_views
from crm_cubedots.views_controller.admins import pre_tasks_views
from crm_cubedots.views_controller.admins import projects_views
from crm_cubedots.views_controller.admins import departments_views
from crm_cubedots.views_controller.admins import task_categories_views
from crm_cubedots.views_controller.admins import admin_users_views
from crm_cubedots.views_controller.admins import projects_categories_views

from crm_cubedots.views_controller.hrs import hr_admin_views
from crm_cubedots.views_controller.hrs import hr_attendence_views
from crm_cubedots.views_controller.hrs import hr_leaves_type
from crm_cubedots.views_controller.hrs import hr_leaves_views

from crm_cubedots.views_controller.moniTasks import moniTasksDashboard_views
from crm_cubedots.views_controller.moniTasks import moni_tasks_views
from crm_cubedots.views_controller.moniTasks import moni_task_leaves_views

from crm_cubedots.views_controller.users import user_profile_views
from crm_cubedots.views_controller.users import user_dashboard_views
from crm_cubedots.views_controller.users import users_tasks_views
from crm_cubedots.views_controller.users import users_leaves_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', views.sign_up),
    #path('/',users_views.userpage, name="user_page"),

    
    path('', views.home, name="home"),
    path('signin/', views.user_login, name="login"),
    path('dashboard/', views.admin_dashboard, name="dashboard"),
    path('logout/', views.user_logout),

    #------Admin Project-Categories Routes ----------
    path('projectsCategories/search/', projects_categories_views.project_categories_search, name = "search_projectCategory"),
    path('admin/projectsCategories/create', projects_categories_views.project_categories_create, name="project_category_create"),
    path('admin/projectsCategories/store', projects_categories_views.project_categories_store, name = "category_store"),
    path('admin/projectsCategories/update/<int:id>', projects_categories_views.project_categories_update,name = "category_update"),
    path('admin/projectsCategories/delete/<int:id>',projects_categories_views.project_categories_destroy,name="category_delete"),
    path('admin/projectsCategories/show/<int:id>', projects_categories_views.project_categories_show, name="category_show"),
    path('admin/projectsCategories', projects_categories_views.project_categories, name="project_category_index"),

    #------Admin Projects Routes ----------
    path('project/search/', projects_views.project_search,name="search_project"),
    path('admin/projects/create', projects_views.project_create, name="project_create"),
    path('admin/projects/store', projects_views.project_store, name="project_store"),
    path('admin/projects/index',projects_views.project_index, name="project_index"),
    path('admin/projects/update/<int:id>',projects_views.project_update, name="project_update"),
    path('admin/projects/delete/<int:id>', projects_views.project_soft_delete, name="project_destroy"),
    path('admin/projects/show/<int:id>', projects_views.project_show, name="project_show"),
 
    #------Admin Departments Routes ----------
    path('department/search/',departments_views.departments_search,name="search_department"),
    path('admin/departments/create',departments_views.departments_create, name="department_create"),
    path('admin/departments/store',departments_views.departments_store, name="department_store"),
    path('admin/departments/index', departments_views.departments_index, name="department_index"),
    path('admin/departments/update/<int:id>', departments_views.departments_update, name="department_update"),
    path('admin/departments/delete/<int:id>', departments_views.departments_soft_delete, name="department_destroy"),
    path('admin/departments/show/<int:id>', departments_views.departments_show, name="department_show"),

    #------Admin Task Categories Routes ----------
    path('taskCategories/search/',task_categories_views.taskCategories_search,name="search_taskCategory"),
    path('admin/taskCategories/create',task_categories_views.taskCategories_create, name="taskCategory_create"),
    path('admin/taskCategories/index', task_categories_views.taskCategories_index, name="taskCategory_index"),
    path('admin/taskCategories/store', task_categories_views.taskCategories_store, name="taskCategory_store"),
    path('admin/taskCategories/show/<int:id>', task_categories_views.taskCategories_show, name="taskCategory_show"),
    path('admin/taskCategories/update/<int:id>', task_categories_views.taskCategories_update, name="taskCategory_update"),
    path('admin/taskCategories/delete/<int:id>',task_categories_views.taskCategories_soft_delete, name="taskCategory_destroy"),
    
    #------Admin Users Routes ----------
    path('admin/users/search/', admin_users_views.users_search,name="search_user"),
    path('admin/users/index', admin_users_views.users_index, name="admin_user_index"),
    path('admin/users/create',admin_users_views.users_create, name="admin_user_create"),
    path('admin/users/store',admin_users_views.users_store, name="admin_user_store"),
    path('admin/users/update/<int:id>', admin_users_views.users_update, name="admin_user_update"),
    path('admin/users/delete/<int:id>', admin_users_views.users_soft_delete, name="admin_user_delete"),
    path('admin/users/profile/<str:id>',admin_users_views.users_profile_pic, name="admin_user_profile"),
    path('admin/users/profile/reset_password/<int:id>',admin_users_views.reset_password, name="reset_password"),

    #------Admin Tasks Routes ----------
    path('tasks/<int:id>/search', admin_tasks_views.tasks_search,name="admin_tasks_search"),
    path('admin/projects/<int:id>/tasks',admin_tasks_views.tasks_index, name="admin_task_index"),
    path('admin/projects/<int:id>/tasks/create', admin_tasks_views.tasks_create, name="admin_task_create"),
    path('admin/projects/<int:id>/tasks/store',admin_tasks_views.tasks_store, name="admin_task_store"),
    path('admin/projects/<int:id>/tasks/show',admin_tasks_views.tasks_show, name="admin_task_show"),
    path('admin/projects/<int:id>/tasks/update',admin_tasks_views.tasks_update, name="admin_task_update"),
    path('admin/projects/<int:id>/tasks/delete',admin_tasks_views.tasks_soft_delete, name="admin_task_delete"),

    #------Admin Dashboard Routes ----------
    path('admin/dashboard/index',admin_dashboard_views.dashboard_index,name='admin_dashboard_index'),
    path('admin/dashboard/projects/counts/<str:status_type>',admin_dashboard_views.projectsCounts, name="project_count"),
    
    #------Admin Pre Tasks Routes ----------
    path('admin/preTasks',pre_tasks_views.pretasks_index,name='pretasks_index'),
    path('admin/preTasks/create',pre_tasks_views.pretask_create,name ='pretask_create'),
    path('admin/preTasks/store',pre_tasks_views.pretask_store,name ='pretask_store'),
    path('admin/preTasks/<int:id>/edit',pre_tasks_views.pretask_update,name ='pretask_update'),
    path('admin/preTasks/search',pre_tasks_views.pretask_search,name ='pretask_search'),
    path('admin/preTasks/<int:id>/delete',pre_tasks_views.pretask_soft_deleted,name ='pretask_delete'),
    path('admin/preTasks/createBulk',pre_tasks_views.pretask_create_bulk_index,name ='pretask_createBulk_index'),
    path('admin/preTasks/createBulk/search',pre_tasks_views.pretask_create_bulk_search,name ='pretask_createBulk_search'),
    path('admin/preTasks/createBulk/store',pre_tasks_views.pretask_create_bulk_store,name ='pretask_createBulk_store'),
    path('admin/preTasks/uploadSheet/store',pre_tasks_views.pretask_upload_sheet_store,name ='pretask_upload_sheet_store'),
    path('admin/preTasks/uploadSheet',pre_tasks_views.pretask_upload_sheet_index,name ='pretask_upload_sheet_index'),
    path('admin/preTasks/downloadTasks',pre_tasks_views.pretask_export_tasks,name ='pretask_export_tasks'),
    path('admin/preTasks/downloadTasks/index',pre_tasks_views.pretask_export_tasks_index,name ='pretask_export_tasks_index'),
    
    #------Users Dashboard Routes ----------
    path('users/dashboard',user_dashboard_views.user_dashboard_index, name="user_dashboard_index"),

    #------Users Profile Routes ----------
    path('users/profile/<int:id>',user_profile_views.user_profile, name="user_profile"),
    path('users/profile/<int:id>/reset_password',user_profile_views.user_profile_reset_password, name='user_reset_password'),



    #------Users Tasks Routes Api----------
    # path('api/users/tasks/<str:id>',users_tasks_views.user_task_api, name="user_tasks"),


    #------Users Tasks Routes ----------
    path('users/tasks',users_tasks_views.user_tasks, name="user_tasks"),
    path('users/search',users_tasks_views.user_tasks_search, name="user_tasks_search"),
    path('users/showProjects/<int:id>',users_tasks_views.user_tasks_showProjects, name="user_tasks_showProjects"),
    path('users/showProjects/search/<int:id>',users_tasks_views.user_tasks_showProjects_search, name="user_tasks_showProjects_search"),
    path('users/show/<int:id>',users_tasks_views.user_tasks_show, name="user_tasks_show"),
    path('users/storeTime/<int:id>',users_tasks_views.user_task_store_time,name="user_task_store_time"),
    path('users/getAjaxTask/<int:id>',users_tasks_views.get_ajax_task,name="get_ajax_task"),
    path('users/getAjaxTaskLog/<int:id>',users_tasks_views.get_ajax_task_log,name="get_ajax_task_log"),
    path('users/getAjaxTaskStatus/<int:id>',users_tasks_views.get_ajax_task_status,name="get_ajax_task_status"),
    path('users/updateStatus/<id>',users_tasks_views.ajax_update_status,name="ajax_update_status"),
    path('users/updateTime/<id>',users_tasks_views.update_time,name="update_time"),

    #-----USER Leave ----------
    path('employee/leaves/dashboard',users_leaves_views.emp_leaves_dashboard,name="emp_leaves_dashboard"),

    path('employee/apply_leaves/store',users_leaves_views.apply_leaves_store, name="emp_apply_leaves_store"),
    path('employee/apply_leaves/create',users_leaves_views.apply_leaves_create, name="emp_apply_leaves_create"),
    path('employee/leave_status/index',users_leaves_views.emp_leaves_index,name="emp_leaves_index"),
    path('employee/leave_status/<int:id>/show',users_leaves_views.emp_leaves_show,name="emp_leaves_show"),
    path('employee/leave_status/<int:id>/update',users_leaves_views.emp_leaves_update,name="emp_leaves_update"),



    #path('json/',admin_tasks_views.json, name="user_profile"),

#------Moni-Tasks Dashboard Routes ----------
    
    path('moni_tasks/dashboard/index', moniTasksDashboard_views.monitasks, name="moni_task"),
    path('moni_tasks/index',moni_tasks_views.moni_tasks_index, name="moni_task_index"),
    path('moni_tasks/search',moni_tasks_views.moni_tasks_search, name="moni_tasks_search"),
    path('moni_tasks/showProjects/<int:id>',moni_tasks_views.moni_tasks_showProjects, name="moni_tasks_showProjects"),
    path('moni_tasks/showProjects/<int:id>/search',moni_tasks_views.moni_tasks_showProjects_search, name="moni_tasks_showProjects_search"),
    path('moni_tasks/show/<int:id>',moni_tasks_views.moni_tasks_show, name="moni_tasks_show"),
    path('moni_tasks/getAjaxTask/<int:id>',moni_tasks_views.moni_tasks_getAjaxTask, name="moni_tasks_getAjaxTask"),
    path('moni_tasks/storeTime/<int:id>',moni_tasks_views.moni_tasks_storeTime,name="moni_tasks_storeTime"),
    path('moni_tasks/getAjaxTaskLog/<int:id>',moni_tasks_views.moni_tasks_getAjaxTaskLog,name="moni_tasks_getAjaxTaskLog"),
    path('moni_tasks/getAjaxTaskStatus/<int:id>',moni_tasks_views.moni_tasks_getAjaxTaskStatus,name="moni_tasks_getAjaxTaskStatus"),
    path('moni_tasks/updateTime/<int:id>',moni_tasks_views.moni_tasks_updateTime,name="moni_tasks_updateTime"),
    path('moni_tasks/updateStatus/<int:id>',moni_tasks_views.moni_tasks_updateStatus,name="moni_tasks_updateStatus"),

#------Moni-Tasks Leaves Routes ---------
    path('moni_tasks/leaves/index',moni_task_leaves_views.leaves_index,name='moni_task_leaves_index'),

#------Moni-Tasks Approve Leaves Routes ----------
    path('moni_tasks/leaves_approval/index',moni_task_leaves_views.approve_leaves_index,name='approve_leaves_index'),
    path('moni_tasks/leaves_approval/<int:id>/update',moni_task_leaves_views.approve_leaves_update,name='approve_leaves_update'),
    path('moni_tasks/leaves_approval/<int:id>/show',moni_task_leaves_views.approve_leaves_show,name='approve_leaves_show'),

#------Moni-Tasks Apply Leaves Routes ----------
    path('moni_tasks/apply_leaves/index',moni_task_leaves_views.apply_leaves_index,name='moni_tasks_apply_leaves_index'),
    path('moni_tasks/apply_leaves/create',moni_task_leaves_views.apply_leaves_create,name='moni_tasks_apply_leaves_create'),
    path('moni_tasks/apply_leaves/store',moni_task_leaves_views.apply_leaves_store,name='moni_tasks_apply_leaves_store'),
    path('moni_tasks/apply_leaves/<int:id>/update',moni_task_leaves_views.apply_leaves_update,name='moni_tasks_apply_leaves_update'),
    path('moni_tasks/apply_leaves/<int:id>/show',moni_task_leaves_views.apply_leaves_show,name='moni_tasks_apply_leaves_show'),

#-----HR Dashboard Routes ----------
    path('hrs/',hr_admin_views.hr_index, name='hr_index'),
    path('hrs/employees',hr_admin_views.hr_employees_index, name='hr_employees'),
    path('hrs/employees/search',hr_admin_views.hr_employees_search, name='hr_employees_search'),
    path('hrs/employees/profile/<int:id>',hr_admin_views.hr_employee_profile, name='hr_employee_profile'),
    path('hrs/employees/update/<int:id>',hr_admin_views.hr_employee_update, name='hr_employee_update'),
    path('hrs/employees/create',hr_admin_views.hr_employee_create, name='hr_employee_create'),
    path('hrs/employees/store',hr_admin_views.hr_employee_store, name='hr_employee_store'),
    path('hrs/employees/delete/<int:id>',hr_admin_views.hr_employee_soft_delete, name='hr_employee_soft_delete'),
    path('hrs/employees/reset_password/<int:id>',hr_admin_views.hr_employee_reset_password, name='hr_employee_reset_password'),

#-----HR Leaves Routes ----------
    path('hrs/hr_admin/leaves/index',hr_leaves_views.hrAdmin_leaves_index,name='hrAdmin_leaves_index'),
    #--- MANAGER ------
    path('hrs/managers/leaves/approval',hr_leaves_views.hrAdmin_leaves_approval_index,name='hrAdmin_leaves_approval_index'),
    path('hrs/managers/leaves/<int:id>/update',hr_leaves_views.hrAdmin_leaves_approval_update,name='hrAdmin_leaves_approval_update'),
    path('hrs/managers/leaves/<int:id>/show',hr_leaves_views.hrAdmin_leaves_approval_show,name='hrAdmin_leaves_approval_show'),
    #----- TL -------
    path('hrs/tl/leaves/approval/index',hr_leaves_views.tl_leaves_approval_index,name='hrAdmin_tl_leaves_approval_index'),
    path('hrs/tl/leaves/approval/<int:id>/show',hr_leaves_views.tl_leaves_approval_show,name='hrAdmin_tl_leaves_approval_show'),

    #----- USER ----
    path('hrs/users/leaves/approval/index',hr_leaves_views.users_leaves_approval_index,name='hrAdmin_users_leaves_approval_index'),
    path('hrs/users/leaves/approval/<int:id>/show',hr_leaves_views.users_leaves_approval_show,name='hrAdmin_users_leaves_approval_show'),


#-----HR Admin Routes ----------
    path('hrs/hr_admin/index',hr_admin_views.hr_admin_index, name='hr_admin_index'),
#-----HR Attendence Routes ----------    
    path('hrs/employees/attendence/index',hr_attendence_views.hr_emlpoyees_attendence_index, name='hr_emlpoyees_attendence_index'),

#-----HR Leaves Types ----------
    path('hr/leaves_type/create',hr_leaves_type.create,name='hr_leaves_type_create'),
    path('hr/leaves_type/store',hr_leaves_type.store,name='hr_leaves_type_store'),
    path('hr/leaves_type/index',hr_leaves_type.index,name='hr_leaves_type_index'),
    path('hr/leaves_type/<int:id>/update',hr_leaves_type.update,name='hr_leaves_type_update'),
    path('hr/leaves_type/<int:id>/delete',hr_leaves_type.soft_delete,name='hr_leaves_type_soft_delete'),





]   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
