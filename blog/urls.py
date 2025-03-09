from django.urls import path

from blog.views.articles import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
)
from blog.views.dashboard import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="blog-home"),
    path("articles/", ArticleListView.as_view(), name="article-list"),
    path("articles/<int:pk>", ArticleDetailView.as_view(), name="article-detail"),
    path("articles/new", ArticleCreateView.as_view(), name="article-create"),
    path(
        "articles/<int:pk>/update", ArticleUpdateView.as_view(), name="article-update"
    ),
    path(
        "articles/<int:pk>/delete", ArticleDeleteView.as_view(), name="article-delete"
    ),
]
