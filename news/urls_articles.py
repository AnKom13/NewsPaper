from django.urls import path, include
from news.views import ArticlesList

from news.views import detail_article



urlpatterns = [

    path('', ArticlesList.as_view(), name='articles_list'),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
# вариант вывода через адрес ex: http://127.0.0.1:8000/news/3
#    path('<int:pk>', PostDetail.as_view()),

# Вариант со списком и ссылками на элементы
# внимание на параметр name. Без него django не может найти функцию
    path('<int:pk>', detail_article, name='detail_article'),

]