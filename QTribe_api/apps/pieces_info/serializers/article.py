"""
文章序列化器
"""

from rest_framework import serializers
from pieces_info.models import ArticleModel, ImageModel
from user.serializers import UserMinimalSerializer


class ArticleSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    default_img_url = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()
    
    class Meta:
        model = ArticleModel
        fields = [
            'id', 'title', 'content', 'default_img', 'default_img_url',
            'running_count', 'star_count', 'collection_count', 'comment_count',
            'user', 'is_top', 'is_starred', 'is_collected',
            'create_time', 'update_time'
        ]
        read_only_fields = ['id', 'running_count', 'star_count', 'collection_count', 'comment_count', 'create_time', 'update_time']
    
    def get_default_img_url(self, obj) -> str:
        if obj.default_img:
            return obj.default_img.url
        return ''
    
    def get_is_starred(self, obj) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.starmodel_set.filter(user=request.user, flag='1').exists()
        return False
    
    def get_is_collected(self, obj) -> bool:
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.collectionmodel_set.filter(user=request.user, flag='1').exists()
        return False


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    default_img_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ArticleModel
        fields = [
            'id', 'title', 'default_img_url', 'running_count',
            'star_count', 'collection_count', 'comment_count',
            'user', 'is_top', 'create_time'
        ]
    
    def get_default_img_url(self, obj) -> str:
        if obj.default_img:
            return obj.default_img.url
        return ''


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ['title', 'content', 'default_img']
    
    def validate_title(self, value):
        if ArticleModel.objects.filter(title=value).exists():
            raise serializers.ValidationError('文章标题已存在')
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        article = ArticleModel.objects.create(user=user, **validated_data)
        return article


class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ['title', 'content', 'default_img', 'is_top']
    
    def validate_title(self, value):
        article = self.instance
        if ArticleModel.objects.filter(title=value).exclude(id=article.id).exists():
            raise serializers.ValidationError('文章标题已存在')
        return value


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['id', 'image', 'image_path', 'create_time']
