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


class TagsResource(resources.ModelResource):
    name = Field(
        column_name='name', attribute='name',)
    color = Field(
        column_name='color', attribute='color',)
    slug = Field(attribute='slug', column_name='slug')
    id = Field(attribute='id', column_name='id')

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


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


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     search_fields = ('name',)
#     inlines = (AmountIngredientInLine,)


@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    search_fields = ('name',)
    inlines = (AmountIngredientInLine,)
    resource_class = IngredientsResource


@admin.register(Tag)
class TagAdmin(ImportExportModelAdmin):
    resource_class = TagsResource
    search_fields = ('name',)


admin.site.register(AmountIngredient)
admin.site.register(Favorite)
admin.site.register(Subscription)
admin.site.register(RecipeTag)
admin.site.register(ShoppingCart)

