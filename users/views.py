from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes, action
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class RegisterUser(ModelViewSet):
    http_method_names = ['post']
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    
class LoginUser(ModelViewSet):
    http_method_names = ['post']
    serializer_class = LoginSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        user = authenticate(email=email, password=password)
        if user is None:
            return Response({"error": "Email or password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
            }
        )
    
class GetUserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(email=self.request.user)
    
    @action(methods=['patch'], detail=False, url_path='update-telegram-chat-id')
    def update_telegram_id(self, request):
        chat_id = request.data.get("chat_id")
        if not chat_id:
            return Response({'error': "chat_id is required when enabling notifications"}, status=status.HTTP_400_BAD_REQUEST)
        user, created = User.objects.get_or_create(id=request.user.id)
        user.telegram_chat_id = chat_id if chat_id else user.telegram_chat_id
        user.save()
        return Response(
            {'message': 'Telegram ID successfully updated'}, status=status.HTTP_200_OK
        )
            
