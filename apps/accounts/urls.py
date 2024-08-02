from django.urls import path
from .views import UserAPIView, LoginView

app_name = 'accounts'

urlpatterns = [
    path('users/', UserAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserAPIView.as_view(), name='user-detail'),
    
    path('login/', LoginView.as_view(), name='login'),
]