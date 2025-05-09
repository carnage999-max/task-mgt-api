from django.urls import path
from .views import LoginUser, RegisterUser
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('login', LoginUser, basename='login')
router.register('register', RegisterUser, basename='register')

urlpatterns = [
    
]

urlpatterns += router.urls
