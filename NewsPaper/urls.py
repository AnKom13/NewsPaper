"""NewsPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from news.models import Category
from news.views import Index
from news.views import NewsCreate, NewsDetail, NewsDelete, NewsEdit, CategoryListView, CategoryDeleteView, subscribe
# from news.views NewsList, NewsSearch
from news.views import ArticleCreate, ArticleDetail, ArticleDelete, ArticleEdit
from accounts.views import ProfileEdit
from news.views import multiply

from rest_framework import routers
from news import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'category', views.CategoryViewset)
router.register(r'post', views.PostViewset)
router.register(r'author', views.AuthorViewset)
router.register(r'user', views.UserViewset)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # подключаем встроенные эндопинты для работы с локализацией
    path('admin/', admin.site.urls),
    path('', include('protect.urls'), name='protect'),
    path('sign/', include('sign.urls'), name='sign'),
    path('accounts/', include('allauth.urls'), name='allauth'),

    # path('pages/', include('django.contrib.flatpages.urls')),

    # path('', NewsList.as_view(), name='start'), # временно (стартовая страница)

    path('news/', include('news.urls_news'), name='news'),
    path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    # после успешного сохранения откроется детальная инфа о посте
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('news/search/', include('news.urls_news'), name='news_search'),

    path('articles/', include('news.urls_articles'), name='articles'),
    path('articles/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='post_delete'),
    path('articles/search/', include('news.urls_articles'), name='article_search'),

    # path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/<int:pk>/edit/', ProfileEdit.as_view(), name='profile_edit'),

    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('api/', include(router.urls), name='api'),
    path('api/category/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    #    path('api/', include('rest_framework.urls', namespace='rest_framework')),

    path('multiply/', multiply, name='multiply'),  # мусор
    #    path('tmp/', include('news.urls_tmp'), name='tmp'),
    path('tmp/', Index.as_view(), name='index')
]
