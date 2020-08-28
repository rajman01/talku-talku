from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from user.models import Profile


def home_view(request):
    return  render(request, 'language/home.html')


def learn_view(request):
    return render(request, 'language/learn.html')


class LearnView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'language/learn.html'
    context_object_name = 'languages'

    def get_queryset(self, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        languages = profile.languages.all()
        return languages

