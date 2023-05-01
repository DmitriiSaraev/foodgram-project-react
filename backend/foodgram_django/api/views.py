from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import RecipeFilter, IngredientFilter
from api.serializers import (
    UserSerializer, RecipeSerializer, TagSerializer, IngredientSerializer,
    AmountIngredientSerializer, ShopingCartSerializer, SubscriptionsSerializer,
    SubscribeSerializer
)
from recipes.models import Recipe, Tag, Ingredient, AmountIngredient, \
    ShoppingCart, Favorite, Subscription
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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class AmountIngredientViewSet(viewsets.ModelViewSet):
    queryset = AmountIngredient.objects.all()
    serializer_class = AmountIngredientSerializer


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        subscriptions = Subscription.objects.values(
            'author_id'
        ).filter(subscriber=self.request.user)
        queryset = User.objects.filter(id__in=subscriptions)
        return queryset


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, pk):
        """ Метод работает с подпиской """
        if request.method == 'POST':
            if Subscription.objects.filter(
                    subscriber=request.user,
                    author__id=pk).exists():
                return Response(
                    'Вы подписаны на этого автора',
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscribe = Subscription.objects.create(
                author_id=pk,
                subscriber=request.user
            )
            if subscribe:
                return Response(
                    'Вы подписались',
                    status=status.HTTP_201_CREATED,
                )

        if request.method == 'DELETE':
            subscribe = Subscription.objects.filter(
                    subscriber=request.user,
                    author__id=pk)
            if subscribe:
                subscribe.delete()
                return Response(
                    'Успешная отписка',
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                'Вы не подписаны',
                status=status.HTTP_400_BAD_REQUEST,
            )

# Получить конкретные записи без кверисета,
# нужно переопределить метод get_quriset
# Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 8/15

