"""
视频视图
"""

import os
import subprocess
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F
from django.conf import settings

from QTribe_api.response import APIResponse, PaginatedResponse
from QTribe_api.exceptions import ValidationError, NotFoundError, PermissionError
from user.models import StarModel, CollectionModel
from pieces_info.models import VideoModel, ImageModel
from pieces_info.serializers import (
    VideoSerializer,
    VideoListSerializer,
    VideoCreateSerializer,
    VideoUpdateSerializer,
)


class VideoListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'is_top', 'is_success']
    search_fields = ['title', 'remark']
    ordering_fields = ['create_time', 'running_count', 'star_count']
    ordering = ['-is_top', '-create_time']
    
    def get_queryset(self):
        return VideoModel.objects.select_related('user').filter(is_success=True)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return VideoCreateSerializer
        return VideoListSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return PaginatedResponse(
                items=serializer.data,
                total=queryset.count(),
                page=int(request.query_params.get('page', 1)),
                page_size=int(request.query_params.get('page_size', 10))
            )
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        video = serializer.save()
        
        video_path = video.video.path
        img_path = os.path.join(settings.MEDIA_ROOT, f'video_covers/{video.id}.jpg')
        
        try:
            self._process_video(video_path, img_path, video)
        except Exception as e:
            pass
        
        return APIResponse.created(
            data=VideoSerializer(video, context={'request': request}).data,
            message='视频上传成功'
        )
    
    def _process_video(self, video_path, img_path, video):
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        
        duration_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i {video_path}'
        screenshot_cmd = f'ffmpeg -ss 00:00:05 -i {video_path} -vframes 1 {img_path}'
        
        result = subprocess.run(duration_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            video.duration_time = f'{minutes:02d}:{seconds:02d}'
        
        screenshot_result = subprocess.run(screenshot_cmd, shell=True, capture_output=True, text=True)
        if screenshot_result.returncode == 0:
            video.img_path = f'/media/video_covers/{video.id}.jpg'
            ImageModel.objects.create(
                image_path=video.img_path,
                video=video,
                user=video.user
            )
        
        video.is_success = True
        video.save()


class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = VideoModel.objects.select_related('user').all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VideoUpdateSerializer
        return VideoSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            video = self.get_object()
        except VideoModel.DoesNotExist:
            raise NotFoundError('视频不存在')
        
        VideoModel.objects.filter(id=video.id).update(running_count=F('running_count') + 1)
        video.refresh_from_db()
        
        serializer = self.get_serializer(video, context={'request': request})
        return APIResponse.success(data=serializer.data)
    
    def update(self, request, *args, **kwargs):
        video = self.get_object()
        
        if video.user != request.user:
            raise PermissionError('只能修改自己的视频')
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(video, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return APIResponse.success(
            data=VideoSerializer(video, context={'request': request}).data,
            message='视频更新成功'
        )
    
    def destroy(self, request, *args, **kwargs):
        video = self.get_object()
        
        if video.user != request.user:
            raise PermissionError('只能删除自己的视频')
        
        video.delete()
        return APIResponse.success(message='视频删除成功')


class MyVideoListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'remark']
    ordering_fields = ['create_time', 'running_count']
    ordering = ['-is_top', '-create_time']
    
    def get_queryset(self):
        return VideoModel.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return PaginatedResponse(
                items=serializer.data,
                total=queryset.count(),
                page=int(request.query_params.get('page', 1)),
                page_size=int(request.query_params.get('page_size', 10))
            )
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return APIResponse.success(data=serializer.data)


class StarVideoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, video_id):
        try:
            video = VideoModel.objects.get(id=video_id)
        except VideoModel.DoesNotExist:
            raise NotFoundError('视频不存在')
        
        star, created = StarModel.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'flag': '1'}
        )
        
        if not created:
            if star.flag == '1':
                star.flag = '0'
                video.star_count = max(0, video.star_count - 1)
            else:
                star.flag = '1'
                video.star_count += 1
        else:
            video.star_count += 1
        
        star.save()
        video.save()
        
        return APIResponse.success(
            data={
                'is_starred': star.flag == '1',
                'star_count': video.star_count
            },
            message='点赞成功' if star.flag == '1' else '取消点赞'
        )


class CollectVideoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, video_id):
        try:
            video = VideoModel.objects.get(id=video_id)
        except VideoModel.DoesNotExist:
            raise NotFoundError('视频不存在')
        
        collection, created = CollectionModel.objects.get_or_create(
            user=request.user,
            video=video,
            defaults={'flag': '1'}
        )
        
        if not created:
            if collection.flag == '1':
                collection.flag = '0'
                video.collection_count = max(0, video.collection_count - 1)
            else:
                collection.flag = '1'
                video.collection_count += 1
        else:
            video.collection_count += 1
        
        collection.save()
        video.save()
        
        return APIResponse.success(
            data={
                'is_collected': collection.flag == '1',
                'collection_count': video.collection_count
            },
            message='收藏成功' if collection.flag == '1' else '取消收藏'
        )


class TopVideoView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, video_id):
        try:
            video = VideoModel.objects.get(id=video_id)
        except VideoModel.DoesNotExist:
            raise NotFoundError('视频不存在')
        
        if video.user != request.user:
            raise PermissionError('只能置顶自己的视频')
        
        video.is_top = 0 if video.is_top == 1 else 1
        video.save()
        
        return APIResponse.success(
            data={'is_top': video.is_top},
            message='置顶成功' if video.is_top else '取消置顶'
        )
