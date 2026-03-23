"""
视图模块
"""

from .article import (
    ArticleListView,
    ArticleDetailView,
    MyArticleListView,
    StarArticleView,
    CollectArticleView,
    TopArticleView,
)
from .video import (
    VideoListView,
    VideoDetailView,
    MyVideoListView,
    StarVideoView,
    CollectVideoView,
    TopVideoView,
)
from .comment import (
    CommentListView,
    CommentDetailView,
    ArticleCommentsView,
    VideoCommentsView,
)
from .message import (
    MessageListView,
    MessageDetailView,
    MarkAllReadView,
    UnreadCountView,
)

__all__ = [
    'ArticleListView',
    'ArticleDetailView',
    'MyArticleListView',
    'StarArticleView',
    'CollectArticleView',
    'TopArticleView',
    'VideoListView',
    'VideoDetailView',
    'MyVideoListView',
    'StarVideoView',
    'CollectVideoView',
    'TopVideoView',
    'CommentListView',
    'CommentDetailView',
    'ArticleCommentsView',
    'VideoCommentsView',
    'MessageListView',
    'MessageDetailView',
    'MarkAllReadView',
    'UnreadCountView',
]
