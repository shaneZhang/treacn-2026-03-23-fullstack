"""
文章URL配置
"""

from django.urls import path
from pieces_info.views.article import (
    ArticleListView,
    ArticleDetailView,
    MyArticleListView,
    StarArticleView,
    CollectArticleView,
    TopArticleView,
)

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('my/', MyArticleListView.as_view(), name='my_articles'),
    path('<int:id>/', ArticleDetailView.as_view(), name='article_detail'),
    path('<int:article_id>/star/', StarArticleView.as_view(), name='star_article'),
    path('<int:article_id>/collect/', CollectArticleView.as_view(), name='collect_article'),
    path('<int:article_id>/top/', TopArticleView.as_view(), name='top_article'),
]
