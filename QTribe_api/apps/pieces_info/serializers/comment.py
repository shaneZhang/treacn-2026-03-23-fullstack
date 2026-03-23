"""
评论序列化器
"""

from rest_framework import serializers
from pieces_info.models import CommentModel
from user.serializers import UserMinimalSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentModel
        fields = [
            'id', 'content', 'user', 'parent', 'replies',
            'create_time', 'update_time'
        ]
        read_only_fields = ['id', 'create_time', 'update_time']
    
    def get_replies(self, obj):
        replies = obj.replies.all()[:5]
        return CommentSerializer(replies, many=True).data


class CommentListSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    reply_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CommentModel
        fields = [
            'id', 'content', 'user', 'parent', 'reply_count',
            'create_time', 'update_time'
        ]
    
    def get_reply_count(self, obj) -> int:
        return obj.replies.count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['content', 'article', 'video', 'life', 'parent']
    
    def validate(self, attrs):
        content_types = ['article', 'video', 'life']
        has_content = any(attrs.get(ct) for ct in content_types)
        
        if not has_content:
            raise serializers.ValidationError('评论必须关联文章、视频或生活分享')
        
        if attrs.get('parent'):
            parent = attrs['parent']
            if parent.article and not attrs.get('article'):
                attrs['article'] = parent.article
            elif parent.video and not attrs.get('video'):
                attrs['video'] = parent.video
            elif parent.life and not attrs.get('life'):
                attrs['life'] = parent.life
        
        return attrs
    
    def create(self, validated_data):
        user = self.context['request'].user
        comment = CommentModel.objects.create(user=user, **validated_data)
        
        if comment.article:
            comment.article.comment_count = comment.article.comments.count()
            comment.article.save(update_fields=['comment_count'])
        elif comment.video:
            comment.video.comment_count = comment.video.comments.count()
            comment.video.save(update_fields=['comment_count'])
        elif comment.life:
            comment.life.comment_count = comment.life.comments.count()
            comment.life.save(update_fields=['comment_count'])
        
        return comment
