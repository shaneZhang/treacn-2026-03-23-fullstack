from rest_framework import serializers
from django.db import transaction
from pieces_info.models import ArticleModel, VideoModel, LifeModel, ImageModel, CommentModel, Message
from user.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_starred = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()
    
    class Meta:
        model = ArticleModel
        fields = ['id', 'title', 'content', 'default_img', 'running_count', 'star_count',
                  'collection_count', 'comment_count', 'user', 'is_top',
                  'create_time', 'update_time', 'is_starred', 'is_collected']
        read_only_fields = ['id', 'running_count', 'star_count', 'collection_count',
                         'comment_count', 'user', 'create_time', 'update_time', 'is_starred', 'is_collected']
    
    def get_is_starred(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            from user.models import StarModel
            return StarModel.objects.filter(user=user, article=obj, flag='1').exists()
        return False
    
    def get_is_collected(self, obj):
        user = self.context.get('request').user if self.context.get('request') else None
        if user and user.is_authenticated:
            from user.models import CollectionModel
            return CollectionModel.objects.filter(user=user, article=obj, flag='1').exists()
        return False

class ArticleCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    
    class Meta:
        model = ArticleModel
        fields = ['title', 'content', 'default_img', 'image']
    
    def create(self, validated_data):
        with transaction.atomic():
            article = ArticleModel.objects.create(
                title=validated_data['title'],
                content=validated_data['content'],
                default_img=validated_data.get('default_img'),
                user=self.context['request'].user
            )
            # 创建ImageModel记录
            if validated_data.get('image') or validated_data.get('default_img'):
                ImageModel.objects.create(
                    image=validated_data.get('image') or validated_data.get('default_img'),
                    user=self.context['request'].user,
                    article=article
                )
            return article

class ArticleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = ['title', 'content', 'default_img']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentModel
        fields = ['id', 'content', 'user', 'comment', 'create_time', 'replies']
        read_only_fields = ['id', 'user', 'create_time', 'replies']
    
    def get_replies(self, obj):
        replies = CommentModel.objects.filter(comment=obj)
        return CommentSerializer(replies, many=True).data

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['content', 'article', 'video', 'life', 'comment']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
