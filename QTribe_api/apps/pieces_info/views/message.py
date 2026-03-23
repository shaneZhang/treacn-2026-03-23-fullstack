"""
消息视图
"""

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import F

from QTribe_api.response import APIResponse, PaginatedResponse
from QTribe_api.exceptions import NotFoundError
from pieces_info.models import Message
from pieces_info.serializers import MessageSerializer, MessageListSerializer


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageListSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['type_1', 'status']
    ordering = ['-create_time']
    
    def get_queryset(self):
        return Message.objects.filter(user_2=self.request.user).select_related('user_1')
    
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


class MessageDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return Message.objects.filter(user_2=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            message = self.get_object()
        except Message.DoesNotExist:
            raise NotFoundError('消息不存在')
        
        if message.status == 1:
            message.status = 0
            message.save()
        
        serializer = self.get_serializer(message, context={'request': request})
        return APIResponse.success(data=serializer.data)


class MarkAllReadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        Message.objects.filter(user_2=request.user, status=1).update(status=0)
        return APIResponse.success(message='已全部标记为已读')


class UnreadCountView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        count = Message.objects.filter(user_2=request.user, status=1).count()
        return APIResponse.success(data={'count': count})
