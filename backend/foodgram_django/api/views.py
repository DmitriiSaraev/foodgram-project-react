from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import RecipeFilter
from api.serializers import (
    UserSerializer, RecipeSerializer, TagSerializer, IngredientSerializer,
    AmountIngredientSerializer
)
from recipes.models import Recipe, Tag, Ingredient, AmountIngredient
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class AmountIngredientViewSet(viewsets.ModelViewSet):
    queryset = AmountIngredient.objects.all()
    serializer_class = AmountIngredientSerializer


# Получить конкретные записи без кверисета,
# нужно переопределить метод get_quriset
# Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 8/15

