from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/check-username/', views.CheckUsernameView.as_view(), name='check-username'),
    path('auth/check-phone/', views.CheckPhoneView.as_view(), name='check-phone'),

    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/avatar/', views.UploadAvatarView.as_view(), name='upload-avatar'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change-password'),

    path('<uuid:id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('<uuid:user_id>/follows/', views.FollowListView.as_view(), name='user-follows'),
    path('follows/', views.FollowCreateView.as_view(), name='follow-create'),

    path('friend-requests/', views.FriendRequestListView.as_view(), name='friend-request-list'),
    path('friend-requests/send/', views.FriendRequestCreateView.as_view(), name='friend-request-create'),
    path('friend-requests/<uuid:request_id>/handle/', views.FriendRequestHandleView.as_view(), name='friend-request-handle'),

    path('friends/', views.FriendshipListView.as_view(), name='friendship-list'),
]
