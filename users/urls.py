from django.urls import path
from .views import login_view, dashboard_view
from django.contrib import admin
from django.urls import path, include
from .views import UserListAPIView 

urlpatterns = [
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
]


