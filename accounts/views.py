from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import render

# Create your views here.
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from accounts.forms import ProfileForm


class ProfileEdit(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    model = User
    template_name = 'profile_edit.html'
