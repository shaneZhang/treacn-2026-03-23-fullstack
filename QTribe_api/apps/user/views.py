"""
用户认证视图
"""

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone

from QTribe_api.response import APIResponse, PaginatedResponse
from QTribe_api.exceptions import ValidationError, AuthenticationError, NotFoundError
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    UserMinimalSerializer,
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return APIResponse.created(
            data={
                'user': UserSerializer(user).data,
                'token': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            },
            message='注册成功'
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            raise ValidationError('用户名和密码不能为空')
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise AuthenticationError('用户名或密码错误')
        
        refresh = RefreshToken.for_user(user)
        
        return APIResponse.success(
            data={
                'user': UserSerializer(user).data,
                'token': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            },
            message='登录成功'
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
        except Exception:
            pass
        
        return APIResponse.success(message='退出成功')


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            raise ValidationError('缺少refresh token')
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            
            return APIResponse.success(
                data={
                    'access': access_token
                }
            )
        except Exception as e:
            raise AuthenticationError('Token无效或已过期')


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return APIResponse.success(data=serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return APIResponse.success(
            data=UserSerializer(user).data,
            message='更新成功'
        )


class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            raise NotFoundError('用户不存在')
        
        serializer = self.get_serializer(user)
        return APIResponse.success(data=serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return APIResponse.success(message='密码修改成功')


class CheckUsernameView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        username = request.query_params.get('username')
        
        if not username:
            raise ValidationError('用户名不能为空')
        
        exists = User.objects.filter(username=username).exists()
        
        return APIResponse.success(
            data={
                'exists': exists,
                'available': not exists
            }
        )


class CheckPhoneView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        phone = request.query_params.get('phone')
        
        if not phone:
            raise ValidationError('手机号不能为空')
        
        exists = User.objects.filter(phone=phone).exists()
        
        return APIResponse.success(
            data={
                'exists': exists,
                'available': not exists
            }
        )


class UploadAvatarView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        avatar = request.FILES.get('avatar')
        
        if not avatar:
            raise ValidationError('请上传头像文件')
        
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if avatar.content_type not in allowed_types:
            raise ValidationError('不支持的文件类型，请上传jpg、png、gif或webp格式图片')
        
        if avatar.size > 5 * 1024 * 1024:
            raise ValidationError('文件大小不能超过5MB')
        
        user = request.user
        user.icon = avatar
        user.save()
        
        return APIResponse.success(
            data={
                'icon_url': user.icon_url
            },
            message='头像上传成功'
        )
