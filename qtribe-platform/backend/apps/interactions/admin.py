from django.contrib import admin
from .models import Like, Collection, Notification


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'comment', 'is_active', 'create_time']
    list_filter = ['is_active', 'create_time']
    search_fields = ['user__username', 'article__title']


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'article', 'is_active', 'create_time']
    list_filter = ['is_active', 'create_time']
    search_fields = ['user__username', 'article__title']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'notification_type', 'is_read', 'create_time']
    list_filter = ['notification_type', 'is_read', 'create_time']
    search_fields = ['sender__username', 'receiver__username', 'content']
