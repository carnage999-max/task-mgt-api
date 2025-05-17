from django.urls import path, include
from .views import TaskViewSet
from rest_framework.routers import DefaultRouter
from users.urls import user_router


router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
user_router.register('tasks', TaskViewSet, basename='user-tasks')
urlpatterns = [
    path('', include(router.urls)),
]

