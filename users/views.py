from django.shortcuts import render

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from users.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework.views import APIView
from users.serializers import UserSerializer
from rest_framework import generics
from .serializers import UserSerializer





@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)

        # Cache user details and role in Redis
        cache.set(f'user:{user.id}', {'username': user.username, 'role': user.role}, timeout=86400)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    user_id = request.user.id
    cached_data = cache.get(f'user:{user_id}')
    
    if cached_data:
        return Response({'message': f"Welcome {cached_data['username']}, your role is {cached_data['role']}"})
    else:
        user = User.objects.get(id=user_id)
        return Response({'message': f"Welcome {user.username}, your role is {user.role}"})

import json
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer

class UserListAPIView(APIView):
    def get(self, request):
        cache_key = "user_list"  # Cache key name
        cached_data = cache.get(cache_key)  # Check if data exists in Redis

        if cached_data:
            # If data is cached, return cached data
            return Response(json.loads(cached_data))

        # If not cached, fetch from DB
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        # Store data in Redis cache for 10 minutes (600 seconds)
        cache.set(cache_key, json.dumps(serializer.data), timeout=600)

        return Response(serializer.data)



class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()
        cache.delete("user_list")  # Clear cache when a new user is created
