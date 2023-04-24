from django_filters import rest_framework as filters

from recipes.models import Recipe


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter(field_name='author__id')
    tag = CharFilterInFilter(field_name='tags__slug', lookup_expr='in')
    is_favorited = filters.BooleanFilter(method='get_is_favorited')

    # is_in_shopping_cart = filters.BooleanFilter(
    #     name='is_active', lookup_expr='exact'
    # )

    class Meta:
        model = Recipe
        fields = ['author', 'tag', 'is_favorited']


    def get_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipes__user=self.request.user)
        return queryset


