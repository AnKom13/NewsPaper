from django import forms
from .models import Post
from django.core.exceptions import ValidationError

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = '__all__' #все поля кроме id
#         # лучше все перечислять, чтобы не вывести поля которые не нужны
#         #fields = ['heading', 'content', 'author', 'category', 'property', ]


class NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['property'].initial = 'N'

    class Meta:
        model = Post
        #fields = '__all__' #все поля кроме id
        # лучше все перечислять, чтобы не вывести поля которые не нужны
        fields = ['heading', 'content', 'author', 'category', 'property', ]

    def clean_property(self):
        pr = self.cleaned_data.get("property")
        if pr != 'N':
            raise ValidationError("Это не статья, а новость")
        return 'N'

class ArticleForm(forms.ModelForm):
    #Т.к. модель одна, а формы 2 (статья и новость), ставлю значение по умолчанию.
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['property'].initial = 'A'



    class Meta:
        model = Post
        fields = ['heading', 'content', 'author', 'category', 'property' ]

    def clean_property(self):
        pr = self.cleaned_data.get("property")
        if pr != 'A':
            raise ValidationError("Это не новость, а статья")
        return 'A'


