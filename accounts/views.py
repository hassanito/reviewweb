from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from . import forms
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.models import User

from shops.models import Review

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

class UserList(generic.ListView):
    mopdel = User
    template_name = "accounts/user_detail.html"
    def get_queryset(self):
        """Return the last five published questions."""
        return User.objects.all()
def UserProfile(request,pk):
    user = User.objects.get(pk=pk)
    template_name="accounts/user_profile.html"

    reviews = Review.objects.filter(reviewer=user)
    for i in reviews:
        print(i)
    context = {
        'user':user,
        'reviews':reviews,
    }
    return render(request, 'accounts/user_profile.html', context)
