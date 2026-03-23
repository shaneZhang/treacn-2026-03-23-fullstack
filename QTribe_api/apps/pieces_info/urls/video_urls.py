"""
视频URL配置
"""

from django.urls import path
from pieces_info.views.video import (
    VideoListView,
    VideoDetailView,
    MyVideoListView,
    StarVideoView,
    CollectVideoView,
    TopVideoView,
)

urlpatterns = [
    path('', VideoListView.as_view(), name='video_list'),
    path('my/', MyVideoListView.as_view(), name='my_videos'),
    path('<int:id>/', VideoDetailView.as_view(), name='video_detail'),
    path('<int:video_id>/star/', StarVideoView.as_view(), name='star_video'),
    path('<int:video_id>/collect/', CollectVideoView.as_view(), name='collect_video'),
    path('<int:video_id>/top/', TopVideoView.as_view(), name='top_video'),
]
