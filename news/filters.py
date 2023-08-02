# import django_filters
# from django_filters import FilterSet
from .models import Post, Category

# Создаем свой набор фильтров для модели Post
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelMultipleChoiceFilter
from django.forms import DateTimeInput


class NewsFilter(FilterSet):
    heading = CharFilter(field_name='heading', label='Шапка', lookup_expr='icontains')
    time_after = DateTimeFilter(
        label='Дата создания после:',
        field_name='time_create',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local', },
        ),
    )

    category = ModelMultipleChoiceFilter(field_name='category', label='Выберите категории:',
                                         queryset=Category.objects.all(), )


# Т.к. я сделал поиск для каждой формы, то этот класс не нужен
# Сделано, чтобы поменять подписи полей на html в части пойскойвой формы
# Если его включить, то порядок вывода 1) все из Meta, 2) поля вне Meta
# class Meta:
#     # В Meta классе мы должны указать Django модель,
#     # в которой будем фильтровать записи.
#     model = Post
#     # В fields мы описываем по каким полям модели
#     # будет производиться фильтрация.
#     fields = {
#         # поиск по названию
#                    'heading': ['icontains'],
#                    'category': ['exact']
#     }


class ArticlesFilter(FilterSet):
    # Т.к. в ТЗ поисковая форма нужна только для новостей, сделал доп. форму для Статей (уже через Meta) для наглядности
    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = {
            # поиск по названию
            'heading': ['icontains'],
            'category': ['exact'],
            # рейтинг  меньше или больше ( 2 поля)
            'rate': ['lt', 'gt'],
        }
