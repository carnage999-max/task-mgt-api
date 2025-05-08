from .serializers import UserSerializer
from .models import User
from rest_framework.viewsets import ModelViewSet


class RegisterUser(ModelViewSet):
    http_method_names = ['post']
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
class LoginUser(ModelViewSet):
    http_method_names = ['post']
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        serilai
