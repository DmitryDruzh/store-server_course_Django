from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='users_image', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification message for {self.user.username} to {self.user.email}'

    def send_verification_email(self):
        link = reverse('email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для пользователя {self.user.username}'
        message = 'Для подтверждения учетной записи перейдите по ссылке {}'.format(verification_link)
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration
