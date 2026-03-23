from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article-list'),
    path('my/', views.MyArticleListView.as_view(), name='my-article-list'),
    path('create/', views.ArticleCreateView.as_view(), name='article-create'),
    path('<uuid:id>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('<uuid:id>/update/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('<uuid:id>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('<uuid:article_id>/toggle-top/', views.ArticleToggleTopView.as_view(), name='article-toggle-top'),

    path('<uuid:article_id>/comments/', views.CommentListView.as_view(), name='comment-list'),
    path('<uuid:article_id>/comments/create/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<uuid:id>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    path('tags/', views.TagListView.as_view(), name='tag-list'),
    path('tags/create/', views.TagCreateView.as_view(), name='tag-create'),

    path('images/upload/', views.ArticleImageUploadView.as_view(), name='article-image-upload'),
]
