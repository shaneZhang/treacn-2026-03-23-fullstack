from django.db import models
from apps.users.models import BaseModel, User
from apps.articles.models import Article, Comment


class Like(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, related_name='likes', verbose_name='文章')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name='likes', verbose_name='评论')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        db_table = 'likes'
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
        unique_together = [
            ['user', 'article'],
            ['user', 'comment'],
        ]

    def __str__(self):
        target = self.article or self.comment
        return f'{self.user.username} 点赞了 {target}'


class Collection(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collections', verbose_name='用户')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='collections', verbose_name='文章')
    is_active = models.BooleanField(default=True, verbose_name='是否有效')

    class Meta:
        db_table = 'collections'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'article']

    def __str__(self):
        return f'{self.user.username} 收藏了 {self.article.title}'


class Notification(BaseModel):
    TYPE_CHOICES = [
        (1, '点赞'),
        (2, '收藏'),
        (3, '评论'),
        (4, '关注'),
        (5, '好友申请'),
        (6, '好友通过'),
        (7, '系统通知'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notifications', verbose_name='接收者')
    notification_type = models.SmallIntegerField(choices=TYPE_CHOICES, verbose_name='类型')
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications', verbose_name='相关文章')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications', verbose_name='相关评论')
    
    content = models.TextField(blank=True, null=True, verbose_name='内容')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')

    class Meta:
        db_table = 'notifications'
        verbose_name = '通知'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}: {self.get_notification_type_display()}'
