from rest_framework import serializers
from .models import Like, Collection, Notification
from apps.users.serializers import UserSerializer
from apps.articles.serializers import ArticleListSerializer, CommentSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article = ArticleListSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'article', 'comment', 'is_active', 'create_time']
        read_only_fields = ['id', 'create_time']


class LikeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['article', 'comment']

    def validate(self, attrs):
        article = attrs.get('article')
        comment = attrs.get('comment')
        
        if not article and not comment:
            raise serializers.ValidationError('请提供文章或评论ID')
        
        if article and comment:
            raise serializers.ValidationError('不能同时点赞文章和评论')
        
        return attrs


class CollectionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    article = ArticleListSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = ['id', 'user', 'article', 'is_active', 'create_time']
        read_only_fields = ['id', 'create_time']


class CollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['article']


class NotificationSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    article = ArticleListSerializer(read_only=True)
    comment = CommentSerializer(read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'sender', 'receiver', 'notification_type', 'notification_type_display',
            'article', 'comment', 'content', 'is_read', 'create_time'
        ]
        read_only_fields = ['id', 'create_time']


class NotificationMarkReadSerializer(serializers.Serializer):
    notification_ids = serializers.ListField(
        child=serializers.UUIDField(),
        required=False
    )
    mark_all = serializers.BooleanField(default=False)
