from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Follow, FriendRequest, Friendship


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'phone', 'email', 'is_verified', 'create_time']
    list_filter = ['is_verified', 'gender', 'is_staff', 'create_time']
    search_fields = ['username', 'phone', 'email']
    readonly_fields = ['create_time', 'update_time']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('phone', 'email', 'avatar', 'signature', 'introduction',
                           'province', 'city', 'district', 'gender', 'birth_date')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'create_time', 'update_time')}),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'create_time']
    list_filter = ['create_time']
    search_fields = ['follower__username', 'following__username']


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'create_time']
    list_filter = ['status', 'create_time']
    search_fields = ['sender__username', 'receiver__username']


@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['user1', 'user2', 'create_time']
    search_fields = ['user1__username', 'user2__username']
