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
import os, markdown
from django.conf import settings
from django.http import HttpResponse


# View to render a Markdown file
def api_docs_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'README.md')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        html = markdown.markdown(content)
        return HttpResponse(html)
    
    
urlpatterns = [
    path('', api_docs_view, name='docs-page'),
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/task/', include('tasks.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
