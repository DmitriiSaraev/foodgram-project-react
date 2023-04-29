from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import RecipeFilter
from api.serializers import (
    UserSerializer, RecipeSerializer, TagSerializer, IngredientSerializer,
    AmountIngredientSerializer, ShopingCartSerializer
)
from recipes.models import Recipe, Tag, Ingredient, AmountIngredient, \
    ShoppingCart, Favorite
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

    # Спринт 8 / 18 → Тема 1 / 3: Django Rest Framework → Урок 14 / 15
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['post', 'delete'], detail=True)
    def shopping_cart(self, request, pk):
        """ Метод работает со списком покупок """
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    user=request.user,
                    recipe__id=pk).exists():
                return Response(
                    'Этот рецепт уже есть в вашем списке покупок',
                    status=status.HTTP_400_BAD_REQUEST,
                )

            shopping_cart = ShoppingCart.objects.create(
                recipe_id=pk,
                user=request.user
            )
            if shopping_cart:
                return Response(
                    'Рецепт успешно добавлен в список покупок',
                    status=status.HTTP_201_CREATED,
                )

        if request.method == 'DELETE':
            shopping_cart = ShoppingCart.objects.filter(
                    user=request.user,
                    recipe__id=pk)
            if shopping_cart:
                shopping_cart.delete()
                return Response(
                    'Рецепт успешно удален из списка покупок',
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                'Этот рецепт уже удален',
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    @action(methods=['post', 'delete'], detail=True)
    def favorite(self, request, pk):
        """ Метод работает со списком избранных рецептов """
        if request.method == 'POST':
            if Favorite.objects.filter(
                    user=request.user,
                    recipe__id=pk).exists():
                return Response(
                    'Этот рецепт уже в избранном',
                    status=status.HTTP_400_BAD_REQUEST,
                )

            favorite = Favorite.objects.create(
                recipe_id=pk,
                user=request.user
            )
            if favorite:
                return Response(
                    'Рецепт успешно добавлен в избранное',
                    status=status.HTTP_201_CREATED,
                )

        if request.method == 'DELETE':
            favorite = Favorite.objects.filter(
                    user=request.user,
                    recipe__id=pk)
            if favorite:
                favorite.delete()
                return Response(
                    'Рецепт успешно удален из избранного',
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                'Этот рецепт уже удален из избранного',
                status=status.HTTP_400_BAD_REQUEST,
            )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class AmountIngredientViewSet(viewsets.ModelViewSet):
    queryset = AmountIngredient.objects.all()
    serializer_class = AmountIngredientSerializer


# Получить конкретные записи без кверисета,
# нужно переопределить метод get_quriset
# Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 8/15

