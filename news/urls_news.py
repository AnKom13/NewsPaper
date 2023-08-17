from django.urls import path
from news.views import NewsList, Index
# from news.views import PostDetail
from news.views import detail_news

urlpatterns = [

    path('', NewsList.as_view(), name='news_list'),

    # Вариант со списком и ссылками на элементы
    # внимание на параметр name. Без него django не может найти функцию
    path('<int:pk>', detail_news, name='detail_news'),

    #временно
    path('ch', Index.as_view(), name='index'),
]
