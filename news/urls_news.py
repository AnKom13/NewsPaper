from django.urls import path, include
from news.views import NewsList
#from news.views import PostDetail
from news.views import detail



urlpatterns = [

    path('', NewsList.as_view(), name='news_list'),

# Вариант со списком и ссылками на элементы
# внимание на параметр name. Без него django не может найти функцию
    path('<int:pk>', detail, name='detail'),

]