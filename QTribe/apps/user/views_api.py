from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import logout
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404

from user.models import UserModel
from QTribe.utils.response import (
    SuccessResponse, CreatedResponse, BadRequestResponse,
    UnauthorizedResponse, NotFoundResponse, APIResponse
)
from .serializers import (
    UserSerializer, UserCreateSerializer, UserLoginSerializer,
    UserUpdateSerializer, AvatarUploadSerializer, PasswordChangeSerializer
)

class AuthViewSet(viewsets.GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_permissions(self):
        if self.action in ['login', 'register', 'refresh_token']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            data = {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return CreatedResponse(data=data, message='注册成功')
        return BadRequestResponse(message=serializer.errors)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            data = {
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return SuccessResponse(data=data, message='登录成功')
        return BadRequestResponse(message=serializer.errors)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return SuccessResponse(message='退出登录成功')
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return BadRequestResponse(message='原密码错误')
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return SuccessResponse(message='密码修改成功')
        return BadRequestResponse(message=serializer.errors)

class UserViewSet(viewsets.GenericViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return SuccessResponse(data=serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(data=UserSerializer(request.user).data, message='更新成功')
        return BadRequestResponse(message=serializer.errors)
    
    @action(detail=False, methods=['post'])
    def upload_avatar(self, request):
        serializer = AvatarUploadSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                # 同时更新ImageModel
                from pieces_info.models import ImageModel
                ImageModel.objects.create(image=request.user.icon, user=request.user)
            return SuccessResponse(data=UserSerializer(request.user).data, message='头像上传成功')
        return BadRequestResponse(message=serializer.errors)
    
    @action(detail=True, methods=['get'])
    def public_profile(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return SuccessResponse(data=serializer.data)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_username(request):
    username = request.data.get('username')
    if not username:
        return BadRequestResponse(message='请提供用户名')
    count = UserModel.objects.filter(username=username).count()
    return SuccessResponse(data={'exists': count > 0, 'count': count})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_phone(request):
    phone = request.data.get('phone')
    if not phone:
        return BadRequestResponse(message='请提供手机号')
    count = UserModel.objects.filter(phone=phone).count()
    return SuccessResponse(data={'exists': count > 0, 'count': count})

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def check_email(request):
    email = request.data.get('email')
    if not email:
        return BadRequestResponse(message='请提供邮箱')
    count = UserModel.objects.filter(email=email).count()
    return SuccessResponse(data={'exists': count > 0, 'count': count})
