from django.urls import path
from news.views import Index


urlpatterns = [
    #временно
    path('', Index.as_view(), name='index'),
]