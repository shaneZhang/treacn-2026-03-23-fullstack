from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import User, Follow, FriendRequest, Friendship
from .serializers import (
    UserSerializer, UserDetailSerializer, UserRegisterSerializer,
    UserLoginSerializer, UserUpdateSerializer, ChangePasswordSerializer,
    FollowSerializer, FollowCreateSerializer, FriendRequestSerializer,
    FriendRequestCreateSerializer, FriendRequestHandleSerializer,
    FriendshipSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'code': 200,
            'message': '注册成功',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data.get('username')
        phone = serializer.validated_data.get('phone')
        password = serializer.validated_data.get('password')
        
        if username:
            user = authenticate(username=username, password=password)
        else:
            try:
                user_obj = User.objects.get(phone=phone)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is None:
            return Response({
                'code': 4001,
                'message': '用户名或密码错误',
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'code': 200,
            'message': '登录成功',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }
        })


class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({
                'code': 200,
                'message': '退出登录成功',
                'data': None
            })
        except Exception:
            return Response({
                'code': 4002,
                'message': '无效的token',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'code': 200,
            'message': '更新成功',
            'data': UserDetailSerializer(instance).data
        })


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({
                'code': 4003,
                'message': '原密码错误',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({
            'code': 200,
            'message': '密码修改成功',
            'data': None
        })


class UploadAvatarView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        avatar = request.FILES.get('avatar')
        if not avatar:
            return Response({
                'code': 4004,
                'message': '请上传头像文件',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user.avatar = avatar
        user.save()
        return Response({
            'code': 200,
            'message': '头像上传成功',
            'data': {'avatar': user.avatar.url}
        })


class CheckUsernameView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if not username:
            return Response({
                'code': 400,
                'message': '请提供用户名',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        exists = User.objects.filter(username=username).exists()
        return Response({
            'code': 200,
            'message': 'success',
            'data': {'exists': exists}
        })


class CheckPhoneView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        phone = request.query_params.get('phone')
        if not phone:
            return Response({
                'code': 400,
                'message': '请提供手机号',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        exists = User.objects.filter(phone=phone).exists()
        return Response({
            'code': 200,
            'message': 'success',
            'data': {'exists': exists}
        })


class FollowListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        follow_type = self.request.query_params.get('type', 'following')
        
        if follow_type == 'following':
            return Follow.objects.filter(follower_id=user_id)
        else:
            return Follow.objects.filter(following_id=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class FollowCreateView(generics.CreateAPIView):
    serializer_class = FollowCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        following_id = request.data.get('following')
        if not following_id:
            return Response({
                'code': 400,
                'message': '请提供被关注用户ID',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if str(request.user.id) == str(following_id):
            return Response({
                'code': 4005,
                'message': '不能关注自己',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            following_id=following_id
        )
        
        if not created:
            follow.delete()
            return Response({
                'code': 200,
                'message': '取消关注成功',
                'data': None
            })
        
        return Response({
            'code': 200,
            'message': '关注成功',
            'data': FollowSerializer(follow).data
        })


class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        request_type = self.request.query_params.get('type', 'received')
        if request_type == 'sent':
            return FriendRequest.objects.filter(sender=self.request.user)
        return FriendRequest.objects.filter(receiver=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        receiver_id = request.data.get('receiver')
        if str(request.user.id) == str(receiver_id):
            return Response({
                'code': 4006,
                'message': '不能向自己发送好友申请',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        existing_request = FriendRequest.objects.filter(
            Q(sender=request.user, receiver_id=receiver_id) |
            Q(sender_id=receiver_id, receiver=request.user)
        ).first()
        
        if existing_request:
            return Response({
                'code': 4007,
                'message': '已存在好友申请或已是好友',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        friend_request = serializer.save(sender=request.user)
        
        return Response({
            'code': 200,
            'message': '好友申请发送成功',
            'data': FriendRequestSerializer(friend_request).data
        })


class FriendRequestHandleView(generics.GenericAPIView):
    serializer_class = FriendRequestHandleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, request_id, *args, **kwargs):
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        action = serializer.validated_data['action']
        
        if action == 'accept':
            friend_request.status = 1
            friend_request.save()
            
            Friendship.objects.get_or_create(
                user1=min(friend_request.sender, friend_request.receiver, key=lambda u: u.id),
                user2=max(friend_request.sender, friend_request.receiver, key=lambda u: u.id)
            )
            
            return Response({
                'code': 200,
                'message': '已同意好友申请',
                'data': None
            })
        else:
            friend_request.status = 2
            friend_request.save()
            return Response({
                'code': 200,
                'message': '已拒绝好友申请',
                'data': None
            })


class FriendshipListView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })
