from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
#@login_required(login_url='profile:login')
#app_name = 'first_app'
# {% url 'app_name:app_url' %}
def createpost_view(request):
        return redirect(reverse('new_signup'))  # use the namespace of the path url
def goto(request):
        return redirect(reverse('index'))