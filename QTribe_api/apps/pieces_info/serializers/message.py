"""
消息序列化器
"""

from rest_framework import serializers
from pieces_info.models import Message
from user.serializers import UserMinimalSerializer


class MessageSerializer(serializers.ModelSerializer):
    user_1 = UserMinimalSerializer(read_only=True)
    user_2 = UserMinimalSerializer(read_only=True)
    type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'user_1', 'user_2', 'type_1', 'type_display',
            'status', 'article', 'video', 'life',
            'comment_1', 'comment_2', 'create_time'
        ]
    
    def get_type_display(self, obj) -> str:
        type_map = {
            '1': '点赞',
            '2': '收藏',
            '3': '评论',
            '4': '关注',
            '5': '好友申请',
            '6': '好友通过',
            '7': '拒绝好友',
            '8': '访问空间',
        }
        return type_map.get(obj.type_1, '未知类型')


class MessageListSerializer(serializers.ModelSerializer):
    user_1 = UserMinimalSerializer(read_only=True)
    type_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'user_1', 'type_1', 'type_display',
            'status', 'create_time'
        ]
    
    def get_type_display(self, obj) -> str:
        type_map = {
            '1': '点赞',
            '2': '收藏',
            '3': '评论',
            '4': '关注',
            '5': '好友申请',
            '6': '好友通过',
            '7': '拒绝好友',
            '8': '访问空间',
        }
        return type_map.get(obj.type_1, '未知类型')
