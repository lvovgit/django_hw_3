from django.contrib.auth.models import User, AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='страна', **NULLABLE)
    token = models.CharField(max_length=15, verbose_name='токен', **NULLABLE)
    token_time = models.DateTimeField(auto_now_add=True, verbose_name='время создания токена', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'
