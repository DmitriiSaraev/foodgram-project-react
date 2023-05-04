from django.contrib import admin

from .models import (AmountIngredient, Favorite, Subscription,
                     Ingredient, Recipe,
                     RecipeTag, ShoppingCart, Tag)


class AmountIngredientInLine(admin.TabularInline):
    model = AmountIngredient


class RecipeTagInLine(admin.TabularInline):
    model = RecipeTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    search_fields = ('author__username', 'name', 'tags__name')
    """inlines - в нем связанные модели."""
    inlines = (AmountIngredientInLine, RecipeTagInLine)
    list_display = (
        'text', 'name', 'cooking_time', 'author',
        'image', 'pub_date', 'favorite_count')

    """Сколько раз добавили рецепт"""
    def favorite_count(self, obj):
        return obj.favorite_recipes.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    inlines = (AmountIngredientInLine,)


admin.site.register(AmountIngredient)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCart)
admin.site.register(Tag)
