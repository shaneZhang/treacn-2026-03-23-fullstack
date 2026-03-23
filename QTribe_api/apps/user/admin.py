from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import UserModel, FocusModel, FriendModel, StarModel, CollectionModel


@admin.register(UserModel)
class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'username', 'email', 'phone', 'is_active', 'is_staff', 'create_time']
    list_filter = ['is_active', 'is_staff', 'sex']
    search_fields = ['username', 'email', 'phone']
    ordering = ['-id']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': ('phone', 'icon', 'personalized_signature', 'personal_introduce',
                      'province', 'city', 'county', 'sex', 'age')
        }),
    )


@admin.register(FocusModel)
class FocusAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'focus_user', 'flag', 'create_time']
    list_filter = ['flag']
    search_fields = ['user__username', 'focus_user__username']


@admin.register(FriendModel)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'friend_user', 'flag', 'create_time']
    list_filter = ['flag']
    search_fields = ['user__username', 'friend_user__username']


@admin.register(StarModel)
class StarAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'flag', 'create_time']
    list_filter = ['flag']
    search_fields = ['user__username']


@admin.register(CollectionModel)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'flag', 'create_time']
    list_filter = ['flag']
    search_fields = ['user__username']
