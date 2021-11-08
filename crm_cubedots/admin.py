from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from crm_cubedots.model.project_categories import ProjectsCategories
from crm_cubedots.model.projects import Projects
from crm_cubedots.model.departments import Departments
from crm_cubedots.model.task_categories import TaskCategories
from crm_cubedots.model.account import Account
from crm_cubedots.forms import UserChangeForms, UserCreationForms

admin.site.register(ProjectsCategories)
admin.site.register(Projects)
admin.site.register(Departments)
admin.site.register(TaskCategories)


class AccountAdmin(UserAdmin):
    form = UserChangeForms
    add_form = UserCreationForms
    model = Account
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    list_filter = ('username', 'email', 'access_group', 'is_superuser')
    readonly_fields = ['date_joined', 'last_login']
    field_sets = (
        ('User', {'fields': ('username', 'email', 'password', 'access_group')}),
        ('Permissions', {'fields': (('is_staff', 'is_active'), 'access_group','delete_on')}),
        )
        
    add_field_sets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', ('password1', 'password2'))
            }),
        ('Permissions', {'fields': (('is_staff', 'is_active'), 'access_group')})
        )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'access_group')
    ordering = ('username', 'email', 'first_name', 'last_name', 'access_group')

admin.site.register(Account, AccountAdmin)    