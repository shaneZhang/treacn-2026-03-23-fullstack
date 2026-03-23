from django.urls import path
from . import views

urlpatterns = [
    path('likes/toggle/', views.LikeToggleView.as_view(), name='like-toggle'),
    path('likes/', views.LikeListView.as_view(), name='like-list'),

    path('collections/toggle/', views.CollectionToggleView.as_view(), name='collection-toggle'),
    path('collections/', views.CollectionListView.as_view(), name='collection-list'),
    path('collections/check/<uuid:article_id>/', views.CollectionCheckView.as_view(), name='collection-check'),

    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('notifications/mark-read/', views.NotificationMarkReadView.as_view(), name='notification-mark-read'),
    path('notifications/<uuid:pk>/delete/', views.NotificationDeleteView.as_view(), name='notification-delete'),
    path('notifications/unread-count/', views.UnreadCountView.as_view(), name='unread-count'),
]
