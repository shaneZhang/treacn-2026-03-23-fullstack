"""
QTribe API URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.user.urls')),
    path('api/v1/articles/', include('apps.pieces_info.urls.article_urls')),
    path('api/v1/videos/', include('apps.pieces_info.urls.video_urls')),
    path('api/v1/comments/', include('apps.pieces_info.urls.comment_urls')),
    path('api/v1/messages/', include('apps.pieces_info.urls.message_urls')),
    path('api/v1/sms/', include('apps.verify_code.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
