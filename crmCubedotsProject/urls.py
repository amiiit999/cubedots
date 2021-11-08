
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'^admin/$', admin.site.urls),
    path(r'', include('crm_cubedots.urls')),
    # path('admin/', admin.site.urls),
    # path('', include('crm_cubedots.urls')),

]

