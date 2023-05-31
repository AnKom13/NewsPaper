from django.urls import path, include
from news.views import NewsList
#from news.views import PostDetail
#from news.views import detail



urlpatterns = [
    path('', NewsList.as_view()),
    # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
    # int — указывает на то, что принимаются только целочисленные значения
# вариант вывода через адрес ex: http://127.0.0.1:8000/news/3

# Вариант со списком и ссылками на элементы
# внимание на параметр name. Без него django не может найти функцию
   # path('<int:pk>', detail, name='detail'),

]