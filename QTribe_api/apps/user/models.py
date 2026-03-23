"""
用户模型
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True


class UserModel(AbstractUser, BaseModel):
    phone = models.CharField(verbose_name='电话号码', max_length=11, unique=True, null=True, blank=True)
    icon = models.ImageField(verbose_name='用户头像', blank=True, null=True, upload_to='avatars/%Y/%m/%d/')
    personalized_signature = models.CharField(verbose_name='个性签名', max_length=256, blank=True, null=True)
    personal_introduce = models.CharField(verbose_name='个人介绍', max_length=1024, blank=True, null=True)
    province = models.CharField(verbose_name='省份', max_length=32, blank=True, null=True)
    city = models.CharField(verbose_name='城市', max_length=32, blank=True, null=True)
    county = models.CharField(verbose_name='县区', max_length=32, blank=True, null=True)
    sex = models.CharField(verbose_name='性别', max_length=2, default='1')
    age = models.IntegerField(verbose_name='年龄', blank=True, null=True)

    class Meta:
        db_table = 't_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username or str(self.id)

    @property
    def icon_url(self) -> str:
        if self.icon:
            return self.icon.url
        return '/static/assets/img/demo/avatar.png'


class FocusModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户', related_name='following')
    focus_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='被关注用户', related_name='followers')
    flag = models.CharField(verbose_name='标志', max_length=2, default='1')

    class Meta:
        db_table = 't_focus_user'
        verbose_name = '关注列表'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'focus_user']

    def __str__(self):
        return f'{self.user.username} -> {self.focus_user.username}'


class FriendModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='发起申请用户', related_name='friend_requests')
    friend_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='通过申请用户', related_name='friends')
    flag = models.CharField(verbose_name='标志', max_length=2, default='1')

    class Meta:
        db_table = 't_friend_user'
        verbose_name = '好友列表'
        verbose_name_plural = verbose_name
        unique_together = ['user', 'friend_user']

    def __str__(self):
        return f'{self.user.username} <-> {self.friend_user.username}'


class StarModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户', related_name='stars')
    video = models.ForeignKey('pieces_info.VideoModel', on_delete=models.CASCADE, verbose_name='点赞视频', blank=True, null=True)
    article = models.ForeignKey('pieces_info.ArticleModel', on_delete=models.CASCADE, verbose_name='点赞文章', blank=True, null=True)
    life = models.ForeignKey('pieces_info.LifeModel', on_delete=models.CASCADE, verbose_name='点赞生活', blank=True, null=True)
    flag = models.CharField(verbose_name='标志', max_length=2, default='1')

    class Meta:
        db_table = 't_star_user'
        verbose_name = '点赞列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} starred'


class CollectionModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name='用户', related_name='collections')
    video = models.ForeignKey('pieces_info.VideoModel', on_delete=models.CASCADE, verbose_name='收藏视频', blank=True, null=True)
    article = models.ForeignKey('pieces_info.ArticleModel', on_delete=models.CASCADE, verbose_name='收藏文章', blank=True, null=True)
    life = models.ForeignKey('pieces_info.LifeModel', on_delete=models.CASCADE, verbose_name='收藏生活', blank=True, null=True)
    flag = models.CharField(verbose_name='标志', max_length=2, default='1')

    class Meta:
        db_table = 't_collection_user'
        verbose_name = '收藏列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user.username} collected'
