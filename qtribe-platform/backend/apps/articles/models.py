from django.db import models
from apps.users.models import BaseModel, User
import uuid


class Article(BaseModel):
    STATUS_CHOICES = [
        (0, '草稿'),
        (1, '已发布'),
        (2, '已下架'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    summary = models.CharField(max_length=500, blank=True, null=True, verbose_name='摘要')
    cover_image = models.ImageField(upload_to='articles/covers/%Y/%m/', blank=True, null=True, verbose_name='封面图')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='作者')
    
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览量')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    collect_count = models.PositiveIntegerField(default=0, verbose_name='收藏数')
    comment_count = models.PositiveIntegerField(default=0, verbose_name='评论数')
    
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1, verbose_name='状态')
    
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='发布时间')

    class Meta:
        db_table = 'articles'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-published_at', '-create_time']

    def __str__(self):
        return self.title


class ArticleImage(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images', verbose_name='文章')
    image = models.ImageField(upload_to='articles/images/%Y/%m/', verbose_name='图片')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='排序')

    class Meta:
        db_table = 'article_images'
        verbose_name = '文章图片'
        verbose_name_plural = verbose_name
        ordering = ['order']


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name='描述')

    class Meta:
        db_table = 'tags'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ArticleTag(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_tags', verbose_name='文章')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='tag_articles', verbose_name='标签')

    class Meta:
        db_table = 'article_tags'
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name
        unique_together = ['article', 'tag']


class Comment(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='作者')
    content = models.TextField(max_length=1000, verbose_name='内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies', verbose_name='父评论')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')

    class Meta:
        db_table = 'comments'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f'{self.author.username}: {self.content[:50]}'
