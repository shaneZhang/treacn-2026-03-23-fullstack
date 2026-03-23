from django.contrib import admin
from pieces_info.models import (
    ArticleModel, VideoModel, LifeModel,
    ImageModel, CommentModel, Message
)


@admin.register(ArticleModel)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'running_count', 'star_count', 'collection_count', 'is_top', 'create_time']
    list_filter = ['is_top', 'create_time']
    search_fields = ['title', 'content', 'user__username']
    ordering = ['-id']


@admin.register(VideoModel)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'running_count', 'star_count', 'is_success', 'is_top', 'create_time']
    list_filter = ['is_success', 'is_top', 'create_time']
    search_fields = ['title', 'remark', 'user__username']
    ordering = ['-id']


@admin.register(LifeModel)
class LifeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'copy', 'star_count', 'is_top', 'is_friend', 'create_time']
    list_filter = ['is_top', 'is_friend', 'create_time']
    search_fields = ['copy', 'user__username']
    ordering = ['-id']


@admin.register(ImageModel)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'image', 'create_time']
    search_fields = ['user__username']
    ordering = ['-id']


@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'article', 'video', 'life', 'create_time']
    list_filter = ['create_time']
    search_fields = ['content', 'user__username']
    ordering = ['-id']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_1', 'user_2', 'type_1', 'status', 'create_time']
    list_filter = ['type_1', 'status', 'create_time']
    search_fields = ['user_1__username', 'user_2__username']
    ordering = ['-id']
