from django import forms
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        # fields = '__all__' #все поля кроме id
        # лучше все перечислять, чтобы не вывести поля которые не нужны
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'last_login',
                  'date_joined',
                  'password',
                  'is_superuser',
                  'is_staff',
                  'is_active',
                  ]
