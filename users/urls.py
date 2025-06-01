from django.urls import path, include
from .views import LoginUser, RegisterUser, GetUserViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter


router = DefaultRouter()

router.register('login', LoginUser, basename='login')
router.register('register', RegisterUser, basename='register')
router.register('user', GetUserViewSet, basename='user')

user_router = NestedDefaultRouter(router, 'user', lookup='user')

urlpatterns = [
    path('', include(router.urls)), 
    path('', include(user_router.urls)),
]
