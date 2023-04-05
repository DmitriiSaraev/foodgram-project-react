from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        null=False,
        blank=False,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        unique=False,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        unique=False,
        null=False,
        blank=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
