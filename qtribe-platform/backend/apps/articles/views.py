from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import Article, ArticleImage, Tag, ArticleTag, Comment
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer, ArticleCreateSerializer,
    ArticleUpdateSerializer, CommentSerializer, CommentCreateSerializer,
    TagSerializer, TagCreateSerializer, ArticleImageSerializer
)
from config.pagination import StandardResultsSetPagination


class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['author', 'is_top', 'status']
    ordering_fields = ['create_time', 'published_at', 'view_count', 'like_count']
    search_fields = ['title', 'content', 'summary']

    def get_queryset(self):
        queryset = Article.objects.filter(
            is_published=True,
            status=1,
            is_deleted=False
        )
        
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(article_tags__tag__name=tag)
        
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset.select_related('author').prefetch_related('article_tags__tag')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(is_deleted=False)
    serializer_class = ArticleDetailSerializer
    lookup_field = 'id'

    def get_permissions(self):
        article = self.get_object()
        if not article.is_published:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        
        serializer = self.get_serializer(instance, context={'request': request})
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class ArticleCreateView(generics.CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article = serializer.save(author=self.request.user)
        if article.is_published:
            article.published_at = timezone.now()
            article.save(update_fields=['published_at'])
        return article

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = self.perform_create(serializer)
        return Response({
            'code': 200,
            'message': '文章创建成功',
            'data': ArticleDetailSerializer(article, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)


class ArticleUpdateView(generics.UpdateAPIView):
    queryset = Article.objects.filter(is_deleted=False)
    serializer_class = ArticleUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if instance.is_published and not instance.published_at:
            instance.published_at = timezone.now()
            instance.save(update_fields=['published_at'])

        return Response({
            'code': 200,
            'message': '文章更新成功',
            'data': ArticleDetailSerializer(instance, context={'request': request}).data
        })


class ArticleDeleteView(generics.DestroyAPIView):
    queryset = Article.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted'])
        return Response({
            'code': 200,
            'message': '文章删除成功',
            'data': None
        })


class MyArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_published', 'status', 'is_top']
    ordering_fields = ['create_time', 'published_at', 'view_count']

    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user,
            is_deleted=False
        ).select_related('author').prefetch_related('article_tags__tag')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class ArticleToggleTopView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, article_id, *args, **kwargs):
        article = get_object_or_404(Article, id=article_id, author=request.user, is_deleted=False)
        article.is_top = not article.is_top
        article.save(update_fields=['is_top'])
        
        return Response({
            'code': 200,
            'message': '置顶状态已更新',
            'data': {'is_top': article.is_top}
        })


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Comment.objects.filter(
            article_id=article_id,
            parent=None,
            is_deleted=False
        ).select_related('author').prefetch_related('replies__author')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, id=article_id, is_deleted=False)
        comment = serializer.save(author=self.request.user, article=article)
        
        article.comment_count += 1
        article.save(update_fields=['comment_count'])
        
        return comment

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'article_id': self.kwargs.get('article_id')})
        serializer.is_valid(raise_exception=True)
        comment = self.perform_create(serializer)
        return Response({
            'code': 200,
            'message': '评论发布成功',
            'data': CommentSerializer(comment, context={'request': request}).data
        }, status=status.HTTP_201_CREATED)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted'])
        
        article = instance.article
        article.comment_count = max(0, article.comment_count - 1)
        article.save(update_fields=['comment_count'])
        
        return Response({
            'code': 200,
            'message': '评论删除成功',
            'data': None
        })


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.filter(is_deleted=False)
    serializer_class = TagSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': serializer.data
        })


class TagCreateView(generics.CreateAPIView):
    queryset = Tag.objects.filter(is_deleted=False)
    serializer_class = TagCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tag = serializer.save()
        return Response({
            'code': 200,
            'message': '标签创建成功',
            'data': TagSerializer(tag).data
        }, status=status.HTTP_201_CREATED)


class ArticleImageUploadView(generics.CreateAPIView):
    serializer_class = ArticleImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        article_id = request.data.get('article_id')
        image = request.FILES.get('image')
        
        if not article_id or not image:
            return Response({
                'code': 400,
                'message': '请提供文章ID和图片',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        article = get_object_or_404(Article, id=article_id, author=request.user, is_deleted=False)
        
        max_order = ArticleImage.objects.filter(article=article).count()
        article_image = ArticleImage.objects.create(
            article=article,
            image=image,
            order=max_order
        )
        
        return Response({
            'code': 200,
            'message': '图片上传成功',
            'data': ArticleImageSerializer(article_image).data
        }, status=status.HTTP_201_CREATED)
