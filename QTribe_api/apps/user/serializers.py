"""
用户序列化器
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    icon_url = serializers.ReadOnlyField(source='icon_url')
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    articles_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'phone', 'icon', 'icon_url',
            'personalized_signature', 'personal_introduce',
            'province', 'city', 'county', 'sex', 'age',
            'followers_count', 'following_count', 'articles_count',
            'create_time', 'update_time'
        ]
        read_only_fields = ['id', 'create_time', 'update_time']
    
    def get_followers_count(self, obj) -> int:
        return obj.followers.filter(flag='1').count()
    
    def get_following_count(self, obj) -> int:
        return obj.following.filter(flag='1').count()
    
    def get_articles_count(self, obj) -> int:
        return obj.article.count()


class UserMinimalSerializer(serializers.ModelSerializer):
    icon_url = serializers.ReadOnlyField(source='icon_url')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'icon_url', 'personalized_signature']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'phone', 'email']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password_confirm': '两次密码不一致'})
        return attrs
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value
    
    def validate_phone(self, value):
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('手机号已注册')
        return value
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'phone', 'icon', 'personalized_signature',
            'personal_introduce', 'province', 'city', 'county', 'sex', 'age'
        ]
    
    def validate_phone(self, value):
        user = self.instance
        if value and User.objects.filter(phone=value).exclude(id=user.id).exists():
            raise serializers.ValidationError('手机号已被其他用户使用')
        return value


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('原密码错误')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password_confirm': '两次密码不一致'})
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class UserFollowSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(source='focus_user')
    
    class Meta:
        model = User
        fields = ['user', 'flag', 'create_time']


class UserFollowerSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(source='user')
    
    class Meta:
        model = User
        fields = ['user', 'flag', 'create_time']
