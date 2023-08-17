from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.exceptions import FieldDoesNotExist

from django.utils.translation import pgettext_lazy

class Author(models.Model):  # наследуемся от класса Model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rate = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rate = self.post_set.aggregate(postRate=Sum('rate'))
        com_rate = self.user.comment_set.aggregate(comRate=Sum('rate'))

        self.rate = post_rate.get('postRate') * 3 + com_rate.get('comRate')
        self.save()

    def __str__(self):
        #        return str(self.user.id) + ' - ' + self.user.username
        return self.user.username

    def get_field(self, field_name):
        try:
            return self._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None


class Category(models.Model):
    #name = models.CharField(max_length=255, unique=True, help_text='Category name')
    name = models.CharField(max_length=255, unique=True, help_text=pgettext_lazy('Proverka', 'Category name'))
    subscribers = models.ManyToManyField(User, related_name='categories')


    #verbose_name = pgettext_lazy('help text for Category model', 'This is the help text'),

    # допишем свойство, которое будет отображать id+1 (учебный пример)
    @property
    def example(self):
        return self.id+1

    def __str__(self):
        return str(self.name)

#    def __str__(self):
#        return gettext_lazy(self.name)
    def get_field(self, field_name):
        try:
            return self._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None


class Post(models.Model):
    CHOICE = [
        ('N', 'Новость'),
        ('A', 'Статья'),
    ]

    property = models.CharField(max_length=1, choices=CHOICE, verbose_name='Тип')
    time_create = models.DateTimeField(auto_now_add=True)
    heading = models.CharField(max_length=255, unique=True, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    rate = models.SmallIntegerField(default=0, verbose_name='Рейтинг')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.ManyToManyField('Category', through='PostCategory', verbose_name='Категория')

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def preview(self):
        #        return self.content[0:123]+'...'
        return '{0}{1}'.format(self.content[0:123], '...')

    def __str__(self):
        #return str(self.id) + ' - ' + self.property + ' - ' + self.preview() + ' - ' + self.heading
        return str(self.heading)
        # return self.preview()

    def get_absolute_url(self):
        # Т.к. статьи и новости лежат в одной модели, а ссылки у них д.б. разные
        # Добавлена проверка
        if str(self.property) == 'N':
            return reverse('news_detail', args=[str(self.id)])
        else:
            return reverse('article_detail', args=[str(self.id)])

    def articles_absolute_url(self):
        return f'/articles/{self.id}'

    def get_field(self, field_name):
        try:
            return self._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_field(self, field_name):
        try:
            return self._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None

class Comment(models.Model):
    time_create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    rate = models.SmallIntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rate += 1
        self.save()

    def dislike(self):
        self.rate -= 1
        self.save()

    def get_field(self, field_name):
        try:
            return self._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None