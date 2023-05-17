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


from news.views import NewsCreate, NewsDetail, NewsDelete, NewsEdit, NewsList, NewsSearch
from news.views import ArticleCreate, ArticleDetail, ArticleDelete, ArticleEdit

from news.views import multiply

urlpatterns = [
    path('admin/', admin.site.urls),

    #path('pages/', include('django.contrib.flatpages.urls')),

    path('', NewsList.as_view(), name='start'), # временно (стартовая страница)

    path('news/', include('news.urls_news'), name='news'),
    path('news/<int:pk>', NewsDetail.as_view(), name='post_detail'),
    path('news/create/', NewsCreate.as_view(), name='news_create'), # после успешного сохранения откроется детальная инфа о посте
    path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('news/search/', include('news.urls_news'), name='news_search'),



    path('articles/', include('news.urls_articles'), name='articles'),
    path('articles/<int:pk>', ArticleDetail.as_view(), name='post_detail'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='post_delete'),
    path('articles/search/', include('news.urls_articles'), name='article_search'),

    path('multiply/', multiply, name='multiply'), # мусор
]
