from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import auth, messages
from django.urls import reverse

from .forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket


# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Пользователь с именем {username} успешно зарегистрирован!')
            return HttpResponseRedirect(reverse('login'))
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():

            form.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form,
               'basket': Basket.objects.filter(user=request.user)}
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
