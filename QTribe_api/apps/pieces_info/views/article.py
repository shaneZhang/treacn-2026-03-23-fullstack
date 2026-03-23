"""
文章视图
"""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

from QTribe_api.response import APIResponse, PaginatedResponse
from QTribe_api.exceptions import ValidationError, NotFoundError, PermissionError
from user.models import StarModel, CollectionModel
from pieces_info.models import ArticleModel
from pieces_info.serializers import (
    ArticleSerializer,
    ArticleListSerializer,
    ArticleCreateSerializer,
    ArticleUpdateSerializer,
)


class ArticleListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user', 'is_top']
    search_fields = ['title', 'content']
    ordering_fields = ['create_time', 'running_count', 'star_count', 'collection_count']
    ordering = ['-is_top', '-create_time']
    
    def get_queryset(self):
        return ArticleModel.objects.select_related('user').all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticleCreateSerializer
        return ArticleListSerializer
    
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
        article = serializer.save()
        
        return APIResponse.created(
            data=ArticleSerializer(article, context={'request': request}).data,
            message='文章发布成功'
        )


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = ArticleModel.objects.select_related('user').all()
    serializer_class = ArticleSerializer
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ArticleUpdateSerializer
        return ArticleSerializer
    
    def retrieve(self, request, *args, **kwargs):
        try:
            article = self.get_object()
        except ArticleModel.DoesNotExist:
            raise NotFoundError('文章不存在')
        
        ArticleModel.objects.filter(id=article.id).update(running_count=F('running_count') + 1)
        article.refresh_from_db()
        
        serializer = self.get_serializer(article, context={'request': request})
        return APIResponse.success(data=serializer.data)
    
    def update(self, request, *args, **kwargs):
        article = self.get_object()
        
        if article.user != request.user:
            raise PermissionError('无权修改此文章')
        
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(article, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return APIResponse.success(
            data=ArticleSerializer(article, context={'request': request}).data,
            message='文章更新成功'
        )
    
    def destroy(self, request, *args, **kwargs):
        article = self.get_object()
        
        if article.user != request.user:
            raise PermissionError('只能删除自己的文章')
        
        article.delete()
        return APIResponse.success(message='文章删除成功')


class MyArticleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['create_time', 'running_count', 'star_count']
    ordering = ['-is_top', '-create_time']
    
    def get_queryset(self):
        return ArticleModel.objects.filter(user=self.request.user)
    
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


class StarArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, article_id):
        try:
            article = ArticleModel.objects.get(id=article_id)
        except ArticleModel.DoesNotExist:
            raise NotFoundError('文章不存在')
        
        star, created = StarModel.objects.get_or_create(
            user=request.user,
            article=article,
            defaults={'flag': '1'}
        )
        
        if not created:
            if star.flag == '1':
                star.flag = '0'
                article.star_count = max(0, article.star_count - 1)
            else:
                star.flag = '1'
                article.star_count += 1
        else:
            article.star_count += 1
        
        star.save()
        article.save()
        
        return APIResponse.success(
            data={
                'is_starred': star.flag == '1',
                'star_count': article.star_count
            },
            message='点赞成功' if star.flag == '1' else '取消点赞'
        )


class CollectArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, article_id):
        try:
            article = ArticleModel.objects.get(id=article_id)
        except ArticleModel.DoesNotExist:
            raise NotFoundError('文章不存在')
        
        collection, created = CollectionModel.objects.get_or_create(
            user=request.user,
            article=article,
            defaults={'flag': '1'}
        )
        
        if not created:
            if collection.flag == '1':
                collection.flag = '0'
                article.collection_count = max(0, article.collection_count - 1)
            else:
                collection.flag = '1'
                article.collection_count += 1
        else:
            article.collection_count += 1
        
        collection.save()
        article.save()
        
        return APIResponse.success(
            data={
                'is_collected': collection.flag == '1',
                'collection_count': article.collection_count
            },
            message='收藏成功' if collection.flag == '1' else '取消收藏'
        )


class TopArticleView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, article_id):
        try:
            article = ArticleModel.objects.get(id=article_id)
        except ArticleModel.DoesNotExist:
            raise NotFoundError('文章不存在')
        
        if article.user != request.user:
            raise PermissionError('只能置顶自己的文章')
        
        article.is_top = 0 if article.is_top == 1 else 1
        article.save()
        
        return APIResponse.success(
            data={'is_top': article.is_top},
            message='置顶成功' if article.is_top else '取消置顶'
        )
