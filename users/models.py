from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Переопределяем джанговский класс User на основе абстрактного юзера."""

    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
