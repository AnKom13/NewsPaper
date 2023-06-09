from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm, ArticleForm
from .models import Post, Category

from .filters import NewsFilter, ArticlesFilter
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404


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


from django.shortcuts import render
from django.urls import reverse_lazy


def detail_article(request, pk):
    post = Post.objects.get(pk__exact=pk)
    return render(request, 'article.html', context={'post': post})


def detail_news(request, pk):
    post = Post.objects.get(pk__exact=pk)
    return render(request, 'news.html', context={'post': post})


# тест
from django.http import HttpResponse

from django.http import HttpResponseRedirect

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
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)
