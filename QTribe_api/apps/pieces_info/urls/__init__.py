"""
URL模块
"""

from .article_urls import urlpatterns as article_urlpatterns
from .video_urls import urlpatterns as video_urlpatterns
from .comment_urls import urlpatterns as comment_urlpatterns
from .message_urls import urlpatterns as message_urlpatterns

__all__ = [
    'article_urlpatterns',
    'video_urlpatterns',
    'comment_urlpatterns',
    'message_urlpatterns',
]
