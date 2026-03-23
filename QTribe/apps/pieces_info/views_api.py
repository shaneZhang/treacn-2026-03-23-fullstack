from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import F

from pieces_info.models import ArticleModel, CommentModel
from QTribe.utils.response import (
    SuccessResponse, CreatedResponse, BadRequestResponse,
    NotFoundResponse, ForbiddenResponse
)
from .serializers import (
    ArticleSerializer, ArticleCreateSerializer,
    ArticleUpdateSerializer, CommentSerializer,
    CommentCreateSerializer
)

class ArticleViewSet(viewsets.GenericViewSet):
    queryset = ArticleModel.objects.all().select_related('user').order_by('-is_top', '-create_time')
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'user__username']
    ordering_fields = ['create_time', 'star_count', 'running_count']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)
    
    def retrieve(self, request, pk=None):
        article = self.get_object()
        article.running_count = F('running_count') + 1
        article.save()
        article.refresh_from_db()
        serializer = self.get_serializer(article)
        return SuccessResponse(data=serializer.data)
    
    def create(self, request):
        serializer = ArticleCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CreatedResponse(data=ArticleSerializer(serializer.instance, context={'request': request}).data, message='发布成功')
        return BadRequestResponse(message=serializer.errors)
    
    def update(self, request, pk=None):
        article = self.get_object()
        if article.user != request.user:
            return ForbiddenResponse(message='无权限修改')
        serializer = ArticleUpdateSerializer(article, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return SuccessResponse(data=ArticleSerializer(article, context={'request': request}).data, message='更新成功')
        return BadRequestResponse(message=serializer.errors)
    
    def destroy(self, request, pk=None):
        article = self.get_object()
        if article.user != request.user:
            return ForbiddenResponse(message='无权限删除')
        article.delete()
        return SuccessResponse(message='删除成功')
    
    @action(detail=False, methods=['get'])
    def my_articles(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)
    
    @action(detail=True, methods=['post'])
    def top(self, request, pk=None):
        article = self.get_object()
        if article.user != request.user:
            return ForbiddenResponse(message='无权限操作')
        article.is_top = 1 if article.is_top == 0 else 0
        article.save()
        return SuccessResponse(message='操作成功')
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        article = self.get_object()
        comments = CommentModel.objects.filter(article=article, comment=None).order_by('-create_time')
        serializer = CommentSerializer(comments, many=True)
        return SuccessResponse(data=serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        article = self.get_object()
        data = request.data.copy()
        data['article'] = article.id
        serializer = CommentCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            article.comment_count = F('comment_count') + 1
            article.save()
            return CreatedResponse(data=CommentSerializer(serializer.instance).data, message='评论成功')
        return BadRequestResponse(message=serializer.errors)

class CommentViewSet(viewsets.GenericViewSet):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def destroy(self, request, pk=None):
        comment = self.get_object()
        if comment.user != request.user:
            return ForbiddenResponse(message='无权限删除')
        comment.delete()
        return SuccessResponse(message='删除成功')
