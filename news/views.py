from django.shortcuts import render

# Create your views here.
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import NewsForm, ArticleForm
from .models import Post

from .filters import NewsFilter, ArticlesFilter


class NewsList(ListView):
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


class ArticlesList(ListView):
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

def detail(request, pk):
    post = Post.objects.get(pk__exact=pk)
    return render(request, 'post.html', context={'post': post})


# тест
from django.http import HttpResponse

from django.http import HttpResponseRedirect

from .models import Post


#Классы новости
class NewsSearch(CreateView):
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

class NewsCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'


class NewsEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')

#Классы статьи

class ArticleCreate(CreateView):
    # Указываем нашу разработанную форму
    form_class = ArticleForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'article_edit.html'


class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'article'


class ArticleEdit(UpdateView):
    form_class = NewsForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')


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
