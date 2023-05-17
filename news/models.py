from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.urls import reverse


class Author(models.Model):  # наследуемся от класса Model
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rate = models.SmallIntegerField(default=0)

    def update_rating(self):
        post_rate = self.post_set.aggregate(postRate=Sum('rate'))
        com_rate = self.user.comment_set.aggregate(comRate=Sum('rate'))

        self.rate = post_rate.get('postRate') * 3 + com_rate.get('comRate')
        self.save()

    def __str__(self):
        return str(self.user.id) + ' - ' + self.user.username

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.name)

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
        return str(self.id) + ' - ' + self.property + ' - ' + self.preview()
        #return self.preview()

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
