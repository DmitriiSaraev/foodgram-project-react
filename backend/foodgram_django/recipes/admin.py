from django.contrib import admin

from .models import (AmountIngredient, Favorite, Subscription, Ingredient, Recipe,
                     RecipeTag, ShoppingCart, Tag)


class AmountIngredientInLine(admin.TabularInline):
    """Для отображения в админке поля ингредиенты."""

    model = AmountIngredient


class RecipetagInLine(admin.TabularInline):
    """Для отображения в админке поля теги."""

    model = RecipeTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Для администрирования модели рецептов."""

    search_fields = ('author__username', 'name', 'tags__name')
    """inlines - это список классов, которые определяют связанные модели, 
       которые могут быть редактированы вместе с моделью "Recipe"."""
    inlines = (AmountIngredientInLine, RecipetagInLine)
    list_display = (
        'text', 'name', 'cooking_time', 'author',
        'image', 'pub_date', 'favorite_count')

    def favorite_count(self, obj):
        return obj.favorite_recipes.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Для администрирования модели ингредиентов."""

    search_fields = ('name',)
    ordering = ('name',)
    inlines = (AmountIngredientInLine,)


admin.site.register(AmountIngredient)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCart)
admin.site.register(Tag)
