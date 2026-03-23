"""
消息URL配置
"""

from django.urls import path
from pieces_info.views.message import (
    MessageListView,
    MessageDetailView,
    MarkAllReadView,
    UnreadCountView,
)

urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('<int:id>/', MessageDetailView.as_view(), name='message_detail'),
    path('read-all/', MarkAllReadView.as_view(), name='mark_all_read'),
    path('unread-count/', UnreadCountView.as_view(), name='unread_count'),
]
