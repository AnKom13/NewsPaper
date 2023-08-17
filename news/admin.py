from django.contrib import admin
from modeltranslation.admin import TranslationAdmin  # импортируем модель амдинки (вспоминаем модуль про переопределение стандартных админ-инструментов)
# Register your models here.

from .models import Author, Category, Post, PostCategory, Comment
# функция меняет название категории
def change_name(modeladmin, request, queryset):
    # это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
    queryset.update(name='####')
change_name.short_description = 'Имя на #' # описание для более понятного представления в админ панеле задаётся, как будто это объект

# создаём новый класс для представления категорий в админке
# class CategoryAdmin(admin.ModelAdmin):
#     # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
#     # проблема: выводит (пытается) кроме полей таблицы вывести еще и связанные с ней таблицы
#     # list_display = [field.name for field in Category._meta.get_fields()] # генерируем список имён всех полей для более красивого отображения
#     #print (list_display)
#     list_display = ('name', 'id', 'example')
#     list_filter = ('name', 'id')  # добавляем примитивные фильтры в нашу админку
# #    search_fields = ('name', 'id')  # тут всё очень похоже на фильтры из запросов в базу
#     search_fields = ['name']   # тут всё очень похоже на фильтры из запросов в базу
#     search_fields = ['name', 'id']   # тут всё очень похоже на фильтры из запросов в базу
#     actions = [change_name]

class CategoryAdmin(TranslationAdmin):
    model = Category


class PostAdmin(TranslationAdmin):
    model = Post


admin.site.register(Post)
admin.site.register(Category)

admin.site.register(Author)
#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Category)
#admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)

#admin.site.unregister(Category)