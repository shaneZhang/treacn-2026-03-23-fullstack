from rest_framework import serializers
from django.contrib.auth import authenticate
from user.models import UserModel, FocusModel, FriendModel, StarModel, CollectionModel
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'phone', 'email', 'icon', 'personalized_signature', 
                  'personal_introduce', 'province', 'city', 'county', 'sex', 'age', 
                  'first_name', 'last_name', 'is_active', 'create_time', 'update_time']
        read_only_fields = ['id', 'is_active', 'create_time', 'update_time']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = UserModel
        fields = ['username', 'phone', 'password', 'password2', 'email']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "两次输入的密码不一致"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        phone = attrs.get('phone')
        password = attrs.get('password')
        
        if not username and not phone:
            raise serializers.ValidationError("用户名或手机号至少提供一个")
        
        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif phone:
            try:
                user_obj = UserModel.objects.get(phone=phone)
                user = authenticate(username=user_obj.username, password=password)
            except UserModel.DoesNotExist:
                raise serializers.ValidationError("用户不存在")
        
        if not user:
            raise serializers.ValidationError("用户名/手机号或密码错误")
        
        if not user.is_active:
            raise serializers.ValidationError("用户已被禁用")
        
        attrs['user'] = user
        return attrs

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['personalized_signature', 'personal_introduce', 'province', 
                  'city', 'county', 'sex', 'age', 'first_name', 'last_name']

class AvatarUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['icon']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "两次输入的密码不一致"})
        return attrs
