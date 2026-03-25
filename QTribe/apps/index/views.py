from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import View

# 平台介绍页面
from pieces_info.models import VideoModel, ArticleModel, LifeModel

from user.models import UserModel, FocusModel

from utils.pagination import paginate_queryset


class StartIt(View):
    def get(self, request):
        return render(request, 'start/index.html')


class HomePage(View):
    def get(self, request):
        return render(request, 'center3.html', {'user': request.user})


# 404页面
class NoFindPage(View):
    def get(self, request):
        return render(request, '404.html')


# 电影页面
class FreeMovie(View):
    def get(self, request):
        return render(request, 'movie/TV_home.html')


# 查看个人资料
class Information(View):
    def get(self, request):
        return render(request, 'user/information.html', {'user': request.user})


# 视频广场
class VideoMall(View):
    def get(self, request):
        # 获取该平台所有视频
        star_ids = []  # 用于筛选用户点赞过的视频，方便前端渲染
        collection_ids = []  # 用于筛选用户收藏过的视频，方便前端渲染
        video_list = VideoModel.objects.all()
        if request.user.is_authenticated:
            for video in video_list:
                objs = request.user.starmodel_set.all()
                for obj in objs:
                    if obj.video == video and obj.flag == '1':
                        star_ids.append(video.id)
            for video in video_list:
                objs = request.user.collectionmodel_set.all()
                for obj in objs:
                    if obj.video == video and obj.flag == '1':
                        collection_ids.append(video.id)

        # 使用分页工具
        context = paginate_queryset(request, video_list, per_page=5)
        context['star_ids'] = star_ids
        context['collection_ids'] = collection_ids
        return render(request, 'public/video_mall.html', context)


# 文章广场
class ArticleMall(View):
    def get(self, request):
        articles = ArticleModel.objects.all()
        star_ids = []  # 用于筛选用户点赞过的视频，方便前端渲染
        collection_ids = []  # 用于筛选用户收藏过的视频，方便前端渲染
        if request.user.is_authenticated:
            for article in articles:
                objs = request.user.starmodel_set.all()
                for obj in objs:
                    if obj.article == article and obj.flag == '1':
                        star_ids.append(article.id)
            for article in articles:
                objs = request.user.collectionmodel_set.all()
                for obj in objs:
                    if obj.article == article and obj.flag == '1':
                        collection_ids.append(article.id)
        # 使用分页工具
        context = paginate_queryset(request, articles, per_page=5)
        context['star_ids'] = star_ids
        context['collection_ids'] = collection_ids
        return render(request, 'public/article_mall.html', context)


class LifeMall(View):
    def get(self, request):
        lives = LifeModel.objects.all()
        star_ids = []  # 用于筛选用户点赞过的视频，方便前端渲染
        collection_ids = []  # 用于筛选用户收藏过的视频，方便前端渲染
        if request.user.is_authenticated:
            for life in lives:
                objs = request.user.starmodel_set.all()
                for obj in objs:
                    if obj.life == life and obj.flag == '1':
                        star_ids.append(life.id)
            for life in lives:
                objs = request.user.collectionmodel_set.all()
                for obj in objs:
                    if obj.life == life and obj.flag == '1':
                        collection_ids.append(life.id)

        # 使用分页工具
        context = paginate_queryset(request, lives, per_page=5)
        context['star_ids'] = star_ids
        context['collection_ids'] = collection_ids
        return render(request, 'public/life_mall.html', context)


# 其他用户
class OtherUser(View):
    def get(self, request):
        focus_ids = []  # 查询用户关注的用户
        friend_ids = []  # 查询用户好友
        icon_ids = []
        if request.user.is_authenticated:
            users = UserModel.objects.exclude(id=request.user.id).all()
            focus_objs = request.user.focusmodel_set.all()
            friend1_objs = request.user.friendmodel_set.all()
            friend2_objs = request.user.friend_user.all()
            for obj in focus_objs:
                if obj.flag == '1':
                    focus_ids.append(obj.focus_user_id)
            # 因为在friend表中两个字段关联的字段名不一样，所以要循环两次
            for obj in friend1_objs:
                if obj.flag == '1':
                    friend_ids.append(obj.friend_user_id)
            for obj in friend2_objs:
                if obj.flag == '1':
                    friend_ids.append(obj.user_id)
        else:
            users = UserModel.objects.all()

        for user in users:
            if user.icon:
                icon_ids.append(user.id)
        # 使用分页工具
        context = paginate_queryset(request, users, per_page=10)
        context['focus_ids'] = focus_ids
        context['friend_ids'] = friend_ids
        context['icon_ids'] = icon_ids
        return render(request, 'user/other_user.html', context)


class OtherDetails(View):
    def get(self, request):
        u_id = int(request.GET.get('u_id'))
        user = UserModel.objects.get(id=u_id)
        return render(request, 'user/center3.html', {'user_': user})
