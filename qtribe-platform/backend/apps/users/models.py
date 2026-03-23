from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_deleted = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    phone = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True, verbose_name='头像')
    signature = models.CharField(max_length=256, blank=True, null=True, verbose_name='个性签名')
    introduction = models.TextField(max_length=1024, blank=True, null=True, verbose_name='个人介绍')
    province = models.CharField(max_length=32, blank=True, null=True, verbose_name='省份')
    city = models.CharField(max_length=32, blank=True, null=True, verbose_name='城市')
    district = models.CharField(max_length=32, blank=True, null=True, verbose_name='区县')
    gender = models.SmallIntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, verbose_name='性别')
    birth_date = models.DateField(blank=True, null=True, verbose_name='出生日期')
    is_verified = models.BooleanField(default=False, verbose_name='是否认证')

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-create_time']

    def __str__(self):
        return self.username


class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='关注者')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='被关注者')

    class Meta:
        db_table = 'user_follows'
        verbose_name = '关注关系'
        verbose_name_plural = verbose_name
        unique_together = ['follower', 'following']


class FriendRequest(BaseModel):
    STATUS_CHOICES = [
        (0, '待处理'),
        (1, '已同意'),
        (2, '已拒绝'),
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests', verbose_name='接收者')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name='状态')
    message = models.CharField(max_length=200, blank=True, null=True, verbose_name='验证消息')

    class Meta:
        db_table = 'user_friend_requests'
        verbose_name = '好友申请'
        verbose_name_plural = verbose_name
        unique_together = ['sender', 'receiver']


class Friendship(BaseModel):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends1', verbose_name='用户1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends2', verbose_name='用户2')

    class Meta:
        db_table = 'user_friendships'
        verbose_name = '好友关系'
        verbose_name_plural = verbose_name
        unique_together = ['user1', 'user2']
