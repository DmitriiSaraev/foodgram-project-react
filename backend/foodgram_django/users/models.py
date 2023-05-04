from django.db import models
from django.contrib.auth.models import AbstractUser


ADMIN = 'admin'
USER = 'user'

ROLE_CHOICES = [(ADMIN, 'admin'), (USER, 'user')]


class User(AbstractUser):
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
    role = models.CharField(
        verbose_name='роль',
        default=USER,
        choices=ROLE_CHOICES,
        max_length=5,
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
