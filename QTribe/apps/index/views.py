from django.shortcuts import render, redirect

from django.views.generic.base import View

from pieces_info.models import VideoModel, ArticleModel, LifeModel

from user.models import UserModel, FocusModel

from QTribe.utils.pagination import get_pagination_data


class StartIt(View):
    def get(self, request):
        return render(request, 'start/index.html')


class HomePage(View):
    def get(self, request):
        return render(request, 'center3.html', {'user': request.user})


class NoFindPage(View):
    def get(self, request):
        return render(request, '404.html')


class FreeMovie(View):
    def get(self, request):
        return render(request, 'movie/TV_home.html')


class Information(View):
    def get(self, request):
        return render(request, 'user/information.html', {'user': request.user})


class VideoMall(View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        star_ids = []
        collection_ids = []
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

        pagination_data = get_pagination_data(video_list, page_number, per_page=5)
        pagination_data['star_ids'] = star_ids
        pagination_data['collection_ids'] = collection_ids
        return render(request, 'public/video_mall.html', pagination_data)


class ArticleMall(View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        articles = ArticleModel.objects.all()
        star_ids = []
        collection_ids = []
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
        pagination_data = get_pagination_data(articles, page_number, per_page=5)
        pagination_data['star_ids'] = star_ids
        pagination_data['collection_ids'] = collection_ids
        return render(request, 'public/article_mall.html', pagination_data)


class LifeMall(View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        lives = LifeModel.objects.all()
        star_ids = []
        collection_ids = []
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

        pagination_data = get_pagination_data(lives, page_number, per_page=5)
        pagination_data['star_ids'] = star_ids
        pagination_data['collection_ids'] = collection_ids
        return render(request, 'public/life_mall.html', pagination_data)


class OtherUser(View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        focus_ids = []
        friend_ids = []
        icon_ids = []
        if request.user.is_authenticated:
            users = UserModel.objects.exclude(id=request.user.id).all()
            focus_objs = request.user.focusmodel_set.all()
            friend1_objs = request.user.friendmodel_set.all()
            friend2_objs = request.user.friend_user.all()
            for obj in focus_objs:
                if obj.flag == '1':
                    focus_ids.append(obj.focus_user_id)
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
        pagination_data = get_pagination_data(users, page_number, per_page=10)
        pagination_data['focus_ids'] = focus_ids
        pagination_data['friend_ids'] = friend_ids
        pagination_data['icon_ids'] = icon_ids
        return render(request, 'user/other_user.html', pagination_data)


class OtherDetails(View):
    def get(self, request):
        u_id = int(request.GET.get('u_id'))
        user = UserModel.objects.get(id=u_id)
        return render(request, 'user/center3.html', {'user_': user})
