import django_filters
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _  # импортируем функцию для перевода

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView

from .forms import NewsForm, ArticleForm
from .models import Post, Category

from .filters import NewsFilter, ArticlesFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from news.serializers import *
from news.models import *
from rest_framework import generics

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ["property"]


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# import logging
# logger = logging.getLogger(__name__)

# class Index(View):
#     def get(self, request):
#         string = _('Hello world')
#
#         # return HttpResponse(string)
#         context = {'string': string}
#         return HttpResponse(render(request, 'tmp.html', context))

# #Пример с переводом полей в админке
# class Index(View):
#     def get(self, request):
#         # . Translators: This message appears on the home page only
#         models = Category.objects.all()
# #        models = Post.objects.all()
#         context = {
#             'models': models,
#         }
#         #print (context)
#         return HttpResponse(render(request, 'tmp2.html', context))

import pytz  # импортируем стандартный модуль для работы с часовыми поясами
from django.utils import timezone
from django.shortcuts import redirect

class Index(View):
    def get(self, request):
        curent_time = timezone.now()

        # .  Translators: This message appears on the home page only
        models = Category.objects.all()

        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'tmp3.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/tmp/')

class NewsList(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'

    # По ТЗ надо выводить список новостей, а не всех постов (кроме новостей есть еще и статьи)
    # Для этого реализован этот фильтр. Если его убрать, тогда queryset вернет все записи
    # queryset = Post.objects.all().filter(property='N')
    paginate_by = 10  # количество записей на странице

    # Переопределяем функцию получения списка новостей
    # @property
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        queryset = Post.objects.filter(property='N')
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)

        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class ArticlesList(LoginRequiredMixin, ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_create'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'articles_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'articles'

    # По ТЗ надо выводить список новостей, а не всех постов (кроме новостей есть еще и статьи)
    # Для этого реализован этот фильтр. Если его убрать, тогда queryset вернет все записи
    # queryset = Post.objects.all().filter(property='N')
    paginate_by = 10  # количество записей на странице

    # Переопределяем функцию получения списка статей
    # @property
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        queryset = Post.objects.filter(property='A')
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = ArticlesFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


def detail_article(request, pk):
    post = Post.objects.get(pk__exact=pk)
    return render(request, 'article.html', context={'post': post})


def detail_news(request, pk):
    post = Post.objects.get(pk__exact=pk)
    return render(request, 'news.html', context={'post': post})


# тест
from django.http import HttpResponse

# from django.http import HttpResponseRedirect

from .models import Post


# Классы новости
class NewsSearch(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'


class NewsCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = NewsForm

    # проверка прав
    permission_required = ('news.add_post',)
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post

    template_name = 'news.html'
    context_object_name = 'news'


class NewsEdit(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


# Классы статьи

# class ArticleCreate(CreateView):
class ArticleCreate(PermissionRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = ArticleForm

    # проверка прав
    permission_required = ('news.add_post',)

    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'article_edit.html'


class ArticleDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    form_class = NewsForm
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


class ArticleSearch(LoginRequiredMixin, CreateView):
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'article_edit.html'


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписались на категорию: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


# мусор
def multiply(request):
    f = request.GET.get('a')
    s = request.GET.get('b')

    try:
        result = int(f) * int(s)
        html = f"<html><body>{f}*{s}={result}</body></html>"
    except (ValueError, TypeError):
        html = "<html><body>Invalid input.</body></html>"

    return HttpResponse(html)
