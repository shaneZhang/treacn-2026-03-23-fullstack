"""
用户URL配置
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTTokenRefreshView
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    TokenRefreshView,
    UserProfileView,
    UserDetailView,
    ChangePasswordView,
    CheckUsernameView,
    CheckPhoneView,
    UploadAvatarView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/password/', ChangePasswordView.as_view(), name='change_password'),
    path('profile/avatar/', UploadAvatarView.as_view(), name='upload_avatar'),
    
    path('check/username/', CheckUsernameView.as_view(), name='check_username'),
    path('check/phone/', CheckPhoneView.as_view(), name='check_phone'),
    
    path('users/<int:id>/', UserDetailView.as_view(), name='user_detail'),
]
