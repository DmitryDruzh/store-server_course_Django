import os
from django.test import TestCase

from datetime import timedelta
from http import HTTPStatus


from django.urls import reverse

from django.utils.timezone import now


from users.models import EmailVerification, User



class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('register')
        self.data = {
            'first_name': 'Dimon',
            'last_name': 'Limon',
            'username': 'dimonlimon',
            'email': 'limon@mail.ru',
            'password1': '1234567pP',
            'password2': '1234567pP'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store | Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, self.data)

        # tests for creating users
        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302 - redirect
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # tests for email_verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        username = self.data['username']
        user = User.objects.create(username=username)
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


# class UserLoginTestCase(TestCase):
#
#     def setUp(self):
#         self.path = reverse('login')
#         self.data = {'username': 'druzh', 'password': '123'}
#
#     def test_user_login_get(self):
#         response = self.client.get(self.path)
#
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(response, 'users/login.html')
#         self.assertEqual(response.context_data['title'], 'Store | Авторизация')
#
#     def test_user_login_post_seccess(self):  #  not done
#         username = self.data['username']
#         password = self.data['password']
#         user = User.objects.create(username=username, password=password)
#
#         self.assertTrue(User.objects.filter(username=username).exists())
#
#         response = self.client.post(self.path, self.data)
#
#         self.assertContains(response, '''Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть
#                                          чувствительны к регистру.''', html=True)
#         self.assertEqual(response.status_code, HTTPStatus.FOUND)
#         self.assertRedirects(response, reverse('index'))


