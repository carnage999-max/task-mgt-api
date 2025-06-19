"""
URL configuration for task_mgt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView
from tasks.views import docs
from django.shortcuts import render
import os
from django.http import HttpResponse, HttpResponseForbidden
import logging


logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def ping_site(request):
    if request.headers.get("X-Cron-Token") != os.getenv("CRON_SECRET_TOKEN"):
        logger.warning(f"Unauthorized ping attempt from {request.META.get('REMOTE_ADDR')}")
        return HttpResponseForbidden("Forbidden")
    logger.info("Ping successful")
    return HttpResponse("Hello World")
    
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/task/', include('tasks.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', docs, name='docs'),
    path('', docs, name='docs'),
    path('ping/', ping_site, name='ping'),
]
