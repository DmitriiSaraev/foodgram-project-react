from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        blank=True,
        verbose_name='Наименование',
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        null=True,
        blank=False,
        verbose_name='Цвет',
    )
    slug = models.CharField(
        max_length=200,
        unique=True,
        null=True,
        blank=False,
        verbose_name='Слаг',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        null=False,
        blank=False,
        verbose_name='Наименование',
    )

    measurement_unit = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Ед. измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        default=1,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='recipes',
    )
    name = models.CharField(
        max_length=200,
        null=False,
        blank=False,
        verbose_name='Наименование',
    )
    image = models.ImageField(upload_to='recipes/')

    text = models.TextField(
        null=False,
        blank=False,
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        blank=False,
        through='AmountIngredient',
        verbose_name='Ингредиенты',
        related_name='recipes',
    )

    tags = models.ManyToManyField(
        Tag,
        blank=False,
        through='RecipeTag',
        verbose_name='Теги',
        related_name='tags',
    )

    cooking_time = models.IntegerField(blank=False)

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'Рецепт: {self.name}, Автор: {self.author}'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Тег рецепта'
        verbose_name_plural = 'Теги рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'tag'),
                name='unique_recipe_tag'),)

    def __str__(self):
        return f'Теги рецепта {self.recipe}'


class AmountIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_to_ingredient',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient_to_recipe',
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'),)

    def __str__(self):
        return f'Список ингредиентов для рецепта {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,

        verbose_name='Пользователь',
        related_name='shopping_cart',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,

        verbose_name='Рецепт',
        related_name='in_shopping_carts',
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart_recipe'),)

    def __str__(self):
        return f'Список покупок пользователя {self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorite_recipes',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorite_recipes',
    )

    class Meta:
        verbose_name = 'Избраный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_recipe'),)

    def __str__(self):
        return f'Избраные рецепты пользователя {self.user}'


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='followings',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='followers',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('subscriber', 'author'),
                name='unique_follow'),)

    def __str__(self):
        return f'Подписки пользоваеля {self.subscriber}'
