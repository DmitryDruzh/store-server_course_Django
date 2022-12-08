from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from common.views import TitleMixin
from products.models import Basket

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import EmailVerification, User

# Create your views here.

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store | Авторизация'

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             messages.success(request, f'Пользователь с именем {username} успешно зарегистрирован!')
#             return HttpResponseRedirect(reverse('login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context)


class UserRegisterCreateView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    title = 'Store | Регистрация'

    def get_success_message(self, cleaned_data):
        return f'Пользователь с ником {cleaned_data["username"]} успешно зарегистрирован!'



# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#
#             form.save()
#             return HttpResponseRedirect(reverse('profile'))
#     else:
#         user_basket = Basket.objects.filter(user=request.user)
#         form = UserProfileForm(instance=request.user)
#     context = {'form': form,
#                'basket': user_basket,
#                }
#     return render(request, 'users/profile.html', context)


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store | Личный кабинет'



    def get_success_url(self):
        return reverse_lazy('profile', args=(self.object.id,))


# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store | Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_vers = EmailVerification.objects.filter(user=user, code=code)
        if email_vers.exists() and not email_vers.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

