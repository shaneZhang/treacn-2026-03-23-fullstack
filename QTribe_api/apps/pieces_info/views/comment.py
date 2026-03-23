"""
评论视图
"""

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from QTribe_api.response import APIResponse, PaginatedResponse
from QTribe_api.exceptions import NotFoundError, PermissionError
from pieces_info.models import CommentModel, ArticleModel, VideoModel, LifeModel
from pieces_info.serializers import (
    CommentSerializer,
    CommentListSerializer,
    CommentCreateSerializer,
)


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user', 'article', 'video', 'life', 'parent']
    ordering_fields = ['create_time']
    ordering = ['-create_time']
    
    def get_queryset(self):
        return CommentModel.objects.select_related('user').all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentListSerializer
    
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
        comment = serializer.save()
        
        return APIResponse.created(
            data=CommentSerializer(comment, context={'request': request}).data,
            message='评论成功'
        )


class CommentDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = CommentModel.objects.select_related('user').all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        try:
            comment = self.get_object()
        except CommentModel.DoesNotExist:
            raise NotFoundError('评论不存在')
        
        serializer = self.get_serializer(comment, context={'request': request})
        return APIResponse.success(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        
        if comment.user != request.user:
            raise PermissionError('只能删除自己的评论')
        
        content_obj = None
        if comment.article:
            content_obj = comment.article
        elif comment.video:
            content_obj = comment.video
        elif comment.life:
            content_obj = comment.life
        
        comment.delete()
        
        if content_obj:
            content_obj.comment_count = max(0, content_obj.comment_count - 1)
            content_obj.save()
        
        return APIResponse.success(message='评论删除成功')


class ArticleCommentsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentListSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-create_time']
    
    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return CommentModel.objects.filter(article_id=article_id, parent__isnull=True)
    
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


class VideoCommentsView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CommentListSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-create_time']
    
    def get_queryset(self):
        video_id = self.kwargs.get('video_id')
        return CommentModel.objects.filter(video_id=video_id, parent__isnull=True)
    
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
