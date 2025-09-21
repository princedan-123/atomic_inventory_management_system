from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status
from django.utils import timezone
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import AdminUser
from .pagination import CustomPagePagination

class Login(APIView):
    """A class based view that implements login."""
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        print(user)
        if not user:
            return Response({
                'error': 'failed authentication'
            }, status=status.HTTP_401_UNAUTHORIZED)
        user_token, created = Token.objects.get_or_create(user=user)
        print(user_token.key)
        if created:
            time = timezone.now()
            print(time)
            local_time = timezone.localtime(time)
            user.last_login = local_time
            print(user.last_login)
            return Response({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': user_token.key,
                'message': f'welcome {user.role}'
                }
            )
        return Response({'message': 'already logged in'})    
        
class Logout(APIView):
    """Logout implementation."""
    def get(self, request):
        user = request.user
        token_object = Token.objects.get(user=user)
        token_object.delete()
        return Response({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "message": 'successfully logged out'
        }, status=status.HTTP_200_OK)

class UserCrud(viewsets.ModelViewSet):
    """A view that performs CRUD operations on User."""
    permission_classes = [IsAuthenticated, AdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagePagination