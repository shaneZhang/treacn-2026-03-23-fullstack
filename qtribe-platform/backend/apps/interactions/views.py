from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import F
from .models import Like, Collection, Notification
from apps.articles.models import Article, Comment
from apps.users.models import User
from .serializers import (
    LikeSerializer, LikeCreateSerializer,
    CollectionSerializer, CollectionCreateSerializer,
    NotificationSerializer, NotificationMarkReadSerializer
)
from config.pagination import StandardResultsSetPagination


class LikeToggleView(generics.GenericAPIView):
    serializer_class = LikeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.validated_data.get('article')
        comment = serializer.validated_data.get('comment')

        with transaction.atomic():
            like, created = Like.objects.get_or_create(
                user=request.user,
                article=article,
                comment=comment,
                defaults={'is_active': True}
            )

            if not created:
                like.is_active = not like.is_active
                like.save()

            if article:
                if like.is_active:
                    Article.objects.filter(id=article.id).update(like_count=F('like_count') + 1)
                    if article.author != request.user:
                        Notification.objects.create(
                            sender=request.user,
                            receiver=article.author,
                            notification_type=1,
                            article=article,
                            content=f'{request.user.username} 点赞了你的文章《{article.title}》'
                        )
                else:
                    Article.objects.filter(id=article.id).update(like_count=F('like_count') - 1)
            elif comment:
                if like.is_active:
                    Comment.objects.filter(id=comment.id).update(like_count=F('like_count') + 1)
                else:
                    Comment.objects.filter(id=comment.id).update(like_count=F('like_count') - 1)

            action = '点赞' if like.is_active else '取消点赞'
            return Response({
                'code': 200,
                'message': f'{action}成功',
                'data': {
                    'is_liked': like.is_active,
                    'like': LikeSerializer(like).data
                }
            })


class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        content_type = self.request.query_params.get('type', 'article')
        if content_type == 'comment':
            return Like.objects.filter(user=self.request.user, comment__isnull=False, is_active=True)
        return Like.objects.filter(user=self.request.user, article__isnull=False, is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().select_related('article', 'comment', 'user')
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


class CollectionToggleView(generics.GenericAPIView):
    serializer_class = CollectionCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        article = serializer.validated_data.get('article')

        with transaction.atomic():
            collection, created = Collection.objects.get_or_create(
                user=request.user,
                article=article,
                defaults={'is_active': True}
            )

            if not created:
                collection.is_active = not collection.is_active
                collection.save()

            if collection.is_active:
                Article.objects.filter(id=article.id).update(collect_count=F('collect_count') + 1)
                if article.author != request.user:
                    Notification.objects.create(
                        sender=request.user,
                        receiver=article.author,
                        notification_type=2,
                        article=article,
                        content=f'{request.user.username} 收藏了你的文章《{article.title}》'
                    )
            else:
                Article.objects.filter(id=article.id).update(collect_count=F('collect_count') - 1)

            action = '收藏' if collection.is_active else '取消收藏'
            return Response({
                'code': 200,
                'message': f'{action}成功',
                'data': {
                    'is_collected': collection.is_active,
                    'collection': CollectionSerializer(collection).data
                }
            })


class CollectionListView(generics.ListAPIView):
    serializer_class = CollectionSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Collection.objects.filter(
            user=self.request.user,
            is_active=True
        ).select_related('article', 'article__author')

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


class CollectionCheckView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, article_id, *args, **kwargs):
        is_collected = Collection.objects.filter(
            user=request.user,
            article_id=article_id,
            is_active=True
        ).exists()

        return Response({
            'code': 200,
            'message': 'success',
            'data': {'is_collected': is_collected}
        })


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        is_read = self.request.query_params.get('is_read')
        queryset = Notification.objects.filter(receiver=self.request.user)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        return queryset.select_related('sender', 'article', 'comment')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        unread_count = queryset.filter(is_read=False).count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['unread_count'] = unread_count
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'code': 200,
            'message': 'success',
            'data': {
                'results': serializer.data,
                'unread_count': unread_count
            }
        })


class NotificationMarkReadView(generics.GenericAPIView):
    serializer_class = NotificationMarkReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mark_all = serializer.validated_data.get('mark_all', False)
        notification_ids = serializer.validated_data.get('notification_ids', [])

        queryset = Notification.objects.filter(receiver=request.user)

        if mark_all:
            queryset.filter(is_read=False).update(is_read=True)
            message = '所有通知已标记为已读'
        elif notification_ids:
            queryset.filter(id__in=notification_ids, is_read=False).update(is_read=True)
            message = '选中通知已标记为已读'
        else:
            return Response({
                'code': 400,
                'message': '请提供通知ID或选择标记全部',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'code': 200,
            'message': message,
            'data': None
        })


class NotificationDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted'])

        return Response({
            'code': 200,
            'message': '通知删除成功',
            'data': None
        })


class UnreadCountView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        unread_count = Notification.objects.filter(
            receiver=request.user,
            is_read=False,
            is_deleted=False
        ).count()

        return Response({
            'code': 200,
            'message': 'success',
            'data': {'unread_count': unread_count}
        })
