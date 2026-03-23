from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from .models import User, Follow, FriendRequest, Friendship


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar', 'signature', 'introduction', 
                  'province', 'city', 'district', 'gender', 'birth_date',
                  'is_verified', 'create_time']
        read_only_fields = ['id', 'is_verified', 'create_time']


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    articles_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'phone', 'email', 'avatar', 'signature', 
                  'introduction', 'province', 'city', 'district', 'gender', 
                  'birth_date', 'is_verified', 'followers_count', 'following_count',
                  'articles_count', 'create_time', 'update_time']
        read_only_fields = ['id', 'phone', 'is_verified', 'create_time', 'update_time']
    
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    def get_following_count(self, obj):
        return obj.following.count()
    
    def get_articles_count(self, obj):
        return obj.articles.filter(is_published=True).count()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(
        validators=[RegexValidator(regex=r'^1[3-9]\d{9}$', message='请输入有效的手机号')]
    )

    class Meta:
        model = User
        fields = ['username', 'phone', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码输入不一致'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if not attrs.get('username') and not attrs.get('phone'):
            raise serializers.ValidationError('请提供用户名或手机号')
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'avatar', 'signature', 'introduction', 
                  'province', 'city', 'district', 'gender', 'birth_date']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次密码输入不一致'})
        return attrs


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'create_time']
        read_only_fields = ['id', 'create_time']


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['following']


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'message', 'create_time']
        read_only_fields = ['id', 'create_time']


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['receiver', 'message']


class FriendRequestHandleSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['accept', 'reject'])


class FriendshipSerializer(serializers.ModelSerializer):
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Friendship
        fields = ['id', 'friend', 'create_time']
        read_only_fields = ['id', 'create_time']

    def get_friend(self, obj):
        request = self.context.get('request')
        if request and request.user == obj.user1:
            return UserSerializer(obj.user2).data
        return UserSerializer(obj.user1).data
