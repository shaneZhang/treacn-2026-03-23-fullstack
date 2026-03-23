"""
视频序列化器
"""

from rest_framework import serializers
from pieces_info.models import VideoModel
from user.serializers import UserMinimalSerializer


class VideoSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    video_url = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    is_collected = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoModel
        fields = [
            'id', 'title', 'video', 'video_url', 'img_path',
            'duration_time', 'remark', 'running_count',
            'star_count', 'collection_count', 'comment_count',
            'user', 'is_top', 'is_success', 'is_starred', 'is_collected',
            'create_time', 'update_time'
        ]
        read_only_fields = ['id', 'running_count', 'star_count', 'collection_count', 'comment_count', 'create_time', 'update_time']
    
    def get_video_url(self, obj) -> str:
        if obj.video:
            return obj.video.url
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


class VideoListSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)
    video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = VideoModel
        fields = [
            'id', 'title', 'video_url', 'img_path', 'duration_time',
            'running_count', 'star_count', 'collection_count', 'comment_count',
            'user', 'is_top', 'create_time'
        ]
    
    def get_video_url(self, obj) -> str:
        if obj.video:
            return obj.video.url
        return ''


class VideoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = ['title', 'video', 'remark']
    
    def create(self, validated_data):
        user = self.context['request'].user
        video = VideoModel.objects.create(user=user, **validated_data)
        return video


class VideoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoModel
        fields = ['title', 'remark', 'is_top']
