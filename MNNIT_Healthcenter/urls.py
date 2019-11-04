from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('hc/', include('healthcenter.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]