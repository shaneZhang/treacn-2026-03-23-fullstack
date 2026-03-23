"""
内容信息模型
"""

from django.db import models
from django.conf import settings


class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True


class ArticleModel(BaseModel):
    title = models.CharField(max_length=100, unique=True, verbose_name='文章标题')
    content = models.TextField(verbose_name='文章内容')
    default_img = models.ImageField(verbose_name='首页图片', blank=True, null=True, upload_to='articles/%Y/%m/%d/')
    running_count = models.IntegerField(verbose_name='浏览次数', default=0)
    star_count = models.IntegerField(default=0, verbose_name='点赞量')
    collection_count = models.IntegerField(default=0, verbose_name='收藏量')
    comment_count = models.IntegerField(default=0, verbose_name='评论量')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者', related_name='article')
    is_top = models.IntegerField(verbose_name='是否置顶', default=0)

    class Meta:
        db_table = 't_article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-id']

    def __str__(self):
        return self.title


class VideoModel(BaseModel):
    video = models.FileField(verbose_name='视频内容', upload_to='videos/%Y/%m/%d/')
    title = models.CharField(verbose_name='视频标题', max_length=100, null=True, blank=True)
    star_count = models.IntegerField(default=0, verbose_name='点赞量')
    collection_count = models.IntegerField(default=0, verbose_name='收藏量')
    comment_count = models.IntegerField(default=0, verbose_name='评论量')
    duration_time = models.CharField(verbose_name='视频时长', max_length=20, null=True, blank=True)
    remark = models.CharField(verbose_name='备注', max_length=200, null=True, blank=True)
    img_path = models.CharField(verbose_name='封面图片', max_length=512, null=True, blank=True)
    running_count = models.IntegerField(verbose_name='播放次数', default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户', on_delete=models.CASCADE, related_name='video')
    is_top = models.IntegerField(verbose_name='是否置顶', default=0)
    is_success = models.BooleanField(verbose_name='是否发布成功', null=True, blank=True, default=True)

    class Meta:
        db_table = 't_video'
        verbose_name = '视频'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-id']

    def __str__(self):
        return self.title or f'视频{self.id}'


class LifeModel(BaseModel):
    copy = models.CharField(verbose_name='文案', max_length=512)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者', related_name='life')
    default_img = models.ImageField(verbose_name='首页图片', blank=True, null=True, upload_to='life/%Y/%m/%d/')
    star_count = models.IntegerField(default=0, verbose_name='点赞量')
    collection_count = models.IntegerField(default=0, verbose_name='收藏量')
    comment_count = models.IntegerField(default=0, verbose_name='评论量')
    is_top = models.IntegerField(verbose_name='是否置顶', default=0)
    is_friend = models.IntegerField(verbose_name='是否仅好友可见', default=0)
    status = models.CharField(verbose_name='作者状态', blank=True, null=True, max_length=4)
    running_count = models.IntegerField(verbose_name='浏览次数', default=0)

    class Meta:
        db_table = 't_life'
        verbose_name = '生活琐事'
        verbose_name_plural = verbose_name
        ordering = ['-is_top', '-id']

    def __str__(self):
        return self.copy[:30] if self.copy else f'生活{self.id}'


class ImageModel(BaseModel):
    image = models.ImageField(verbose_name='图片内容', blank=True, null=True, upload_to='images/%Y/%m/%d/')
    image_path = models.CharField(verbose_name='图片相对路径', max_length=512, blank=True, null=True)
    video = models.ForeignKey(VideoModel, verbose_name='视频', on_delete=models.CASCADE, blank=True, null=True, related_name='images')
    article = models.ForeignKey(ArticleModel, verbose_name='文章', on_delete=models.CASCADE, blank=True, null=True, related_name='images')
    life = models.ForeignKey(LifeModel, on_delete=models.CASCADE, verbose_name='生活琐事', blank=True, null=True, related_name='images')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 't_image'
        verbose_name = '图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.image.name if self.image else str(self.id)


class CommentModel(BaseModel):
    content = models.CharField(verbose_name='评论内容', max_length=512)
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    life = models.ForeignKey(LifeModel, on_delete=models.CASCADE, verbose_name='生活琐事', blank=True, null=True, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='用户', on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', verbose_name='父评论', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')

    class Meta:
        db_table = 't_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.content[:30]


class Message(BaseModel):
    user_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='发起动作的人', related_name='sent_messages')
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE, blank=True, null=True)
    video = models.ForeignKey(VideoModel, on_delete=models.CASCADE, blank=True, null=True)
    comment_1 = models.ForeignKey(CommentModel, on_delete=models.CASCADE, blank=True, null=True, related_name='message_comment_1')
    comment_2 = models.ForeignKey(CommentModel, on_delete=models.CASCADE, blank=True, null=True, related_name='message_comment_2')
    life = models.ForeignKey(LifeModel, on_delete=models.CASCADE, verbose_name='生活琐事', blank=True, null=True)
    user_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='接收消息的人', related_name='received_messages')
    status = models.IntegerField(verbose_name='状态 0.已读 1.未读', default=1)
    type_1 = models.CharField(verbose_name='信息类型', max_length=4, default='1')

    class Meta:
        db_table = 't_message'
        verbose_name = '通知信息'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f'{self.user_1} -> {self.user_2}'
