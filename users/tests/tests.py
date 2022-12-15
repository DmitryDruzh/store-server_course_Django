import os
from django.test import TestCase

from datetime import timedelta
from http import HTTPStatus

from django.urls import reverse

from django.utils.timezone import now
from users.tasks import send_email_verification

from users.models import EmailVerification, User


class BaseTestCase(TestCase):
    def setUp(self):
        self.path_register = reverse('register')
        self.path_login = reverse('login')
        self.user = {
            'first_name': 'Dimon',
            'last_name': 'Limon',
            'username': 'dimonlimon',
            'email': 'limon@mail.ru',
            'password1': '1234567pP',
            'password2': '1234567pP'
        }
        self.login_data = {'username': 'dimonlimon', 'password': '1234567pP'}


class UserRegistrationViewTestCase(BaseTestCase):
    def test_user_registration_get(self):
        response = self.client.get(self.path_register)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store | Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        username = self.user['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path_register, self.user)

        # tests for creating users

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302 - redirect
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # tests for email_verification
        # user = User.objects.filter(username=username).last()
        # task = send_email_verification.delay(user.id)
        # result = task.get()
        # email_verification = EmailVerification.objects.filter(user__username=username)
        # self.assertTrue(email_verification.exists())
        # self.assertEqual(
        #     email_verification.first().expiration.date(),
        #     (now() + timedelta(hours=48)).date()
        # )

    def test_user_registration_post_error(self):
        username = self.user['username']
        User.objects.create(username=username)
        response = self.client.post(self.path_register, self.user)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginTestCase(BaseTestCase):
    def test_user_login_get(self):
        response = self.client.get(self.path_login)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEqual(response.context_data['title'], 'Store | Авторизация')

    def test_user_login_post_seccess(self):
        self.client.post(self.path_register, self.user)
        user = User.objects.filter(username=self.user['username']).last()
        user.is_active = True
        user.save()

        response = self.client.post(self.path_login, self.login_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_post_seccess_error(self):
        response = self.client.post(self.path_login, {'username': 'kaka', 'password': 'malyaka'})
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response,
                            '''Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.''')


class ProfileTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.client.post(self.path_register, self.user)
        self.client.post(self.path_login, self.login_data)
        self.user_profile = User.objects.filter(username=self.user['username']).last()

    def test_user_profile_get(self):
        path_profile = reverse('profile', args=(self.user_profile.id,))
        response = self.client.get(path_profile)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertEqual(response.context_data['title'], 'Store | Личный кабинет')

    def test_user_profile_post_success(self):
        path_profile = reverse('profile', args=(self.user_profile.id,))
        response_get = self.client.get(path_profile)
        form = response_get.context['form']
        data = form.initial
        data['first_name'] = 'kaka'
        data['last_name'] = 'sraka'
        del data['image']
        response = self.client.post(path_profile, data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response_get.context['form'].initial['first_name'], 'kaka')
        self.assertEqual(response_get.context['form'].initial['last_name'], 'sraka')
