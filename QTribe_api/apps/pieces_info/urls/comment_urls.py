"""
评论URL配置
"""

from django.urls import path
from pieces_info.views.comment import (
    CommentListView,
    CommentDetailView,
    ArticleCommentsView,
    VideoCommentsView,
)

urlpatterns = [
    path('', CommentListView.as_view(), name='comment_list'),
    path('<int:id>/', CommentDetailView.as_view(), name='comment_detail'),
    path('article/<int:article_id>/', ArticleCommentsView.as_view(), name='article_comments'),
    path('video/<int:video_id>/', VideoCommentsView.as_view(), name='video_comments'),
]
