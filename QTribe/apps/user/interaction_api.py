from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from user.models import StarModel, CollectionModel, FocusModel
from pieces_info.models import ArticleModel, VideoModel, LifeModel
from QTribe.utils.response import (
    SuccessResponse, BadRequestResponse,
    NotFoundResponse
)

class InteractionViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = StarModel.objects.all()
    
    def get_content_object(self, content_type, content_id):
        model_map = {
            'article': ArticleModel,
            'video': VideoModel,
            'life': LifeModel,
        }
        model = model_map.get(content_type)
        if not model:
            return None
        return get_object_or_404(model, pk=content_id)
    
    @action(detail=False, methods=['post'])
    def star(self, request):
        content_type = request.data.get('type')
        content_id = request.data.get('id')
        
        if not content_type or not content_id:
            return BadRequestResponse(message='缺少必要参数')
        
        content_obj = self.get_content_object(content_type, content_id)
        if not content_obj:
            return NotFoundResponse(message='内容不存在')
        
        user = request.user
        
        with transaction.atomic():
            star_kwargs = {'user': user, content_type: content_obj}
            star_obj = StarModel.objects.filter(**star_kwargs).first()
            if star_obj:
                if star_obj.flag == '1':
                    star_obj.flag = '0'
                    content_obj.star_count = F('star_count') - 1
                    message = '取消点赞成功'
                else:
                    star_obj.flag = '1'
                    content_obj.star_count = F('star_count') + 1
                    message = '点赞成功'
                star_obj.save()
            else:
                StarModel.objects.create(**{**star_kwargs, 'flag': '1'})
                content_obj.star_count = F('star_count') + 1
                message = '点赞成功'
            content_obj.save()
        
        return SuccessResponse(message=message)
    
    @action(detail=False, methods=['post'])
    def collect(self, request):
        content_type = request.data.get('type')
        content_id = request.data.get('id')
        
        if not content_type or not content_id:
            return BadRequestResponse(message='缺少必要参数')
        
        content_obj = self.get_content_object(content_type, content_id)
        if not content_obj:
            return NotFoundResponse(message='内容不存在')
        
        user = request.user
        
        with transaction.atomic():
            collect_kwargs = {'user': user, content_type: content_obj}
            collect_obj = CollectionModel.objects.filter(**collect_kwargs).first()
            if collect_obj:
                if collect_obj.flag == '1':
                    collect_obj.flag = '0'
                    content_obj.collection_count = F('collection_count') - 1
                    message = '取消收藏成功'
                else:
                    collect_obj.flag = '1'
                    content_obj.collection_count = F('collection_count') + 1
                    message = '收藏成功'
                collect_obj.save()
            else:
                CollectionModel.objects.create(**{**collect_kwargs, 'flag': '1'})
                content_obj.collection_count = F('collection_count') + 1
                message = '收藏成功'
            content_obj.save()
        
        return SuccessResponse(message=message)
    
    @action(detail=False, methods=['get'])
    def star_list(self, request):
        user = request.user
        content_type = request.query_params.get('type', 'article')
        
        filter_kwargs = {
            'user': user,
            'flag': '1',
            f'{content_type}__isnull': False
        }
        
        star_objs = StarModel.objects.filter(**filter_kwargs)
        content_list = [getattr(obj, content_type) for obj in star_objs]
        
        from pieces_info.serializers import ArticleSerializer
        serializer = ArticleSerializer(content_list, many=True, context={'request': request})
        return SuccessResponse(data=serializer.data)
    
    @action(detail=False, methods=['get'])
    def collection_list(self, request):
        user = request.user
        content_type = request.query_params.get('type', 'article')
        
        filter_kwargs = {
            'user': user,
            'flag': '1',
            f'{content_type}__isnull': False
        }
        
        collect_objs = CollectionModel.objects.filter(**filter_kwargs)
        content_list = [getattr(obj, content_type) for obj in collect_objs]
        
        from pieces_info.serializers import ArticleSerializer
        serializer = ArticleSerializer(content_list, many=True, context={'request': request})
        return SuccessResponse(data=serializer.data)
