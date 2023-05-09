from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import (AmountIngredient, Favorite, Subscription,
                     Ingredient, Recipe,
                     RecipeTag, ShoppingCart, Tag)


class IngredientsResource(resources.ModelResource):
    name = Field(
        column_name='name', attribute='name',)
    measurement_unit = Field(
        column_name='measurement_unit', attribute='measurement_unit',)
    id = Field(attribute='id', column_name='id')

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


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
class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientsResource
    list_display = ('name', 'measurement_unit', 'id')
    search_fields = ('name',)
    empty_value_display = 'не заполнено'


admin.site.register(AmountIngredient)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCart)
admin.site.register(Tag)

