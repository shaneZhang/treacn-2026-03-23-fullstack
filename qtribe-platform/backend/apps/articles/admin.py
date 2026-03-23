from django.contrib import admin
from .models import Article, ArticleImage, Tag, ArticleTag, Comment


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1


class ArticleTagInline(admin.TabularInline):
    model = ArticleTag
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'view_count', 'like_count', 'collect_count', 'is_top', 'is_published', 'create_time']
    list_filter = ['is_published', 'is_top', 'status', 'create_time']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['view_count', 'like_count', 'collect_count', 'comment_count', 'create_time', 'update_time']
    inlines = [ArticleImageInline, ArticleTagInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'create_time']
    search_fields = ['name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'author', 'content', 'like_count', 'create_time']
    list_filter = ['create_time']
    search_fields = ['content', 'author__username', 'article__title']
