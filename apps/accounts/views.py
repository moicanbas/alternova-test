from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.accounts.models import CustomUser
from .serializers import UserSerializer
from .models import *
from .serializers import *
from apps.core.views import BaseModelView

class UserAPIView(BaseModelView):
    model = CustomUser
    serializer_class = UserSerializer
    
    
    
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(
                CustomUser, username=request.data['username'])

            if not user.check_password(request.data['password']):
                return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            serializer = UserSerializer(instance=user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Usuario o contraseña incorrectos', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
