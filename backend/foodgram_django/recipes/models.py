from django.db import models
import datetime

from foodgram_django.users.models import User

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        blank=True,
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        null=True,
        blank=False,
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=False,
    )


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
    )

    measurement_unit = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default=1,
        null=False,
        blank=False,
    )
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
    )
    image = models.BinaryField(

    )
    text = models.TextField(
        null=False,
        blank=False,
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        null=False,
        blank=False,
    )

    tags = models.ManyToManyField(
        Tag,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )

    cooking_time = models.IntegerField(blank=False)

    pub_date =



