import os
import subprocess

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse, Http404
from django.shortcuts import redirect, render
from django.views import View
from haystack.query import EmptySearchQuerySet
from haystack.views import SearchView

from pieces_info.models import VideoModel, ImageModel

from user.models import StarModel, CollectionModel

from QTribe.tasks import send_message
from QTribe.utils.pagination import get_pagination_data, get_search_pagination_data


class UploadVideo(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'pieces/upload_video.html')

    def post(self, request):
        title = request.POST.get('title')
        remark = request.POST.get('remark')
        video_path = request.FILES.get('video')

        if not video_path:
            return JsonResponse({'code': 401})

        video_obj = VideoModel.objects.create(title=title, remark=remark, video=video_path, user=request.user)
        video_operator(request, video_obj.id,
                       video_path=os.path.join(settings.BASE_DIR2, 'media', video_obj.video.name),
                       img_path=os.path.join(settings.BASE_DIR2, 'media', f'{video_obj.video.name}{video_obj.id}.jpg'))

        return JsonResponse({'code': 200})


def run_cmd(cmd1, cmd2):
    """运行命令"""
    flag1 = False
    flag2 = False
    play_time = '0'
    result1 = subprocess.run(cmd1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk', shell=True)
    result2 = subprocess.run(cmd2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding='gbk', shell=True)

    if result1.returncode == 0:
        print('播放时长命令完成')
        flag1 = True
        long_time = result1.stdout
        play_time = long_time[:long_time.find('.')]
    else:
        print('播放时长命令执行错误')
        print(result1)
    if result2.returncode == 0:
        print('截取图片命令完成')
        flag2 = True
    else:
        print('截取图片命令执行错误')
        print(result2)

    if flag1 and flag2:
        return True, int(play_time)
    else:
        return False, int(play_time)


def video_operator(request, video_id, video_path, img_path):
    """视频处理,就是拼凑好两条ffmpeg的命令"""
    cmd1 = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i {video_path}'
    cmd2 = f'ffmpeg -ss 00:00:05 -i {video_path} -vframes 1 {img_path}'
    print(cmd1)
    print(cmd2)
    result = run_cmd(cmd1, cmd2)

    if result[0]:
        image_name = os.path.basename(img_path)
        image_path = '/media/' + image_name
        play_time = '%02d:%02d' % (int(result[1] / 60), result[1] % 60)
        with transaction.atomic():
            video = VideoModel.objects.filter(id=video_id).update(img_path=image_path, duration_time=play_time,
                                                                  is_success=True)

            ImageModel.objects.create(image_path=image_path, video_id=video_id, user=request.user)


class MyVideo(LoginRequiredMixin, View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        video_list = VideoModel.objects.filter(user__id=request.user.id)
        pagination_data = get_pagination_data(video_list, page_number, per_page=5)
        return render(request, 'pieces/my_video.html', pagination_data)


class PlayVideo(View):
    def post(self, request):
        v_id = int(request.POST.get('v_id'))
        VideoModel.objects.filter(id=v_id).update(running_count=F('running_count') + 1)
        return JsonResponse({"data": "success"})


class StarVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        args = request.GET.get('args')
        current_page = int(request.GET.get('current_page'))
        q = request.GET.get('q')
        video = VideoModel.objects.get(id=v_id)
        try:
            is_star = StarModel.objects.get(user_id=request.user.id, video_id=v_id)
            flag = is_star.flag
        except:
            is_star = 0
        if is_star and flag == '1':
            video.star_count -= 1
            video.save()
            is_star.flag = '0'
            is_star.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'star':
                try:
                    return redirect(f'/pieces/star_video_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/star_video_list?page_number={current_page - 1}')
            if args == 'collect':
                return redirect(f'/pieces/collect_video_list?page_number={current_page}')
            if args == 'search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')

        else:
            video.star_count += 1
            video.save()
            data = {'u_id': request.user.id, 'type_2': 'star_video', 'p_id': v_id}
            send_message.delay(data)
            if not is_star:
                StarModel.objects.create(user=request.user, video=video, flag='1')
            else:
                is_star.flag = '1'
                is_star.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'collect':
                return redirect(f'/pieces/collect_video_list?page_number={current_page}')
            if args == 'search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')


class CollectVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        current_page = int(request.GET.get('current_page'))
        args = request.GET.get('args')
        q = request.GET.get('q')
        video = VideoModel.objects.get(id=v_id)
        try:
            is_collect = CollectionModel.objects.get(user_id=request.user.id, video_id=v_id)
            flag = is_collect.flag
        except:
            is_collect = 0
        if is_collect and flag == '1':
            video.collection_count -= 1
            video.save()
            is_collect.flag = '0'
            is_collect.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'collect':
                try:
                    return redirect(f'/pieces/collect_video_list?page_number={current_page}')
                except:
                    return redirect(f'/pieces/collect_video_list?page_number={current_page - 1}')
            if args == 'star':
                return redirect(f'/pieces/star_video_list?page_number={current_page}')
            if args == 'search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')
        else:
            video.collection_count += 1
            video.save()
            data = {'u_id': request.user.id, 'type_2': 'collect_video', 'p_id': v_id}
            send_message.delay(data)
            if not is_collect:
                CollectionModel.objects.create(user=request.user, video=video, flag='1')
            else:
                is_collect.flag = '1'
                is_collect.save()
            if args == 'mall':
                return redirect(f'/index/video_mall?page_number={current_page}')
            if args == 'star':
                return redirect(f'/pieces/star_video_list?page_number={current_page}')
            if args == 'search':
                return redirect(f'/pieces/search_video/?page={current_page}&q={q}')


class TopVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        is_top = int(request.GET.get('is_top'))
        current_page = int(request.GET.get('current_page'))
        if is_top == 1:
            VideoModel.objects.filter(id=v_id).update(is_top=0)
            return redirect(f'/pieces/my_video?page_number={current_page}')
        if is_top == 0:
            VideoModel.objects.filter(id=v_id).update(is_top=1)
            return redirect(f'/pieces/my_video?page_number={current_page}')


class DeleteVideo(View):
    def get(self, request):
        v_id = int(request.GET.get('v_id'))
        current_page = int(request.GET.get('current_page'))
        VideoModel.objects.filter(id=v_id).delete()
        try:
            return redirect(f'/pieces/my_video?page_number={current_page}')
        except:
            return redirect(f'/pieces/my_video?page_number={current_page - 1}')


class StarVideoList(LoginRequiredMixin, View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        star_ids = []
        objs = request.user.starmodel_set.all()
        for obj in objs:
            if obj.flag == '1':
                star_ids.append(obj.video_id)
        video_list = VideoModel.objects.filter(id__in=star_ids)
        collection_ids = []
        for video in video_list:
            objs = request.user.collectionmodel_set.all()
            for obj in objs:
                if obj.video == video and obj.flag == '1':
                    collection_ids.append(video.id)
        pagination_data = get_pagination_data(video_list, page_number, per_page=2)
        pagination_data['collection_ids'] = collection_ids
        return render(request, 'pieces/star_video.html', pagination_data)


class CollectVideoList(LoginRequiredMixin, View):
    def get(self, request):
        page_number = int(request.GET.get('page_number', 1))
        collection_ids = []
        objs = request.user.collectionmodel_set.all()
        for obj in objs:
            if obj.flag == '1':
                collection_ids.append(obj.video_id)
        video_list = VideoModel.objects.filter(id__in=collection_ids)
        star_ids = []
        for video in video_list:
            objs = request.user.starmodel_set.all()
            for obj in objs:
                if obj.video == video and obj.flag == '1':
                    star_ids.append(video.id)
        pagination_data = get_pagination_data(video_list, page_number, per_page=2)
        pagination_data['star_ids'] = star_ids
        return render(request, 'pieces/collect_video.html', pagination_data)


class VideoSearchView(SearchView):

    template = 'search/video_search.html'
    results = EmptySearchQuerySet()
    results_per_page = 2

    def __init__(self):
        from haystack.query import SearchQuerySet
        sqs = SearchQuerySet().using('video')
        super(VideoSearchView, self).__init__(searchqueryset=sqs)

    def get_query(self):
        queryset = super(VideoSearchView, self).get_query()
        return queryset

    def get_results(self):
        result = []
        for obj in self.form.search():
            if obj.model_name == 'videomodel':
                result.append(obj)
        return result

    def get_context(self):
        (paginator, page) = self.build_page()
        pagination_data = get_search_pagination_data(paginator, page)
        piece_list = []
        star_ids = []
        collection_ids = []
        for video in page:
            piece_list.append(video.object)
            if self.request.user.is_authenticated:
                stars_obj = video.object.starmodel_set.all()
                collections_obj = video.object.collectionmodel_set.all()
                for obj in stars_obj:
                    if obj.user == self.request.user:
                        star_ids.append(obj.video_id)
                for obj in collections_obj:
                    if obj.user == self.request.user:
                        collection_ids.append(obj.video_id)

        context = {
            "query": self.query,
            "form": self.form,
            "page": page,
            "piece_list": piece_list,
            "paginator": paginator,
            "q": self.get_query(),
            "suggestion": None,
            "star_ids": star_ids,
            "collection_ids": collection_ids,
        }
        context.update(pagination_data)

        if (
            hasattr(self.results, "query")
            and self.results.query.backend.include_spelling
        ):
            context["suggestion"] = self.form.get_suggestion()
        return context
