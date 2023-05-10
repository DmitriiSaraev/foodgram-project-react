from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend
from api.filters import RecipeFilter, IngredientFilter
from api.paginations import Pagination
from api.serializers import (
    UserSerializer,
    RecipeSerializer,
    TagSerializer,
    IngredientSerializer,
    AmountIngredientSerializer,
    SubscriptionsSerializer,
    SubscribeSerializer,
)
from recipes.models import (
    Recipe,
    Tag,
    Ingredient,
    AmountIngredient,
    ShoppingCart,
    Favorite,
    Subscription,
)
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = Pagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise exceptions.PermissionDenied(
                "Нельзя просто так взять и удалить чужой рецепт!")
        instance.delete()

    @action(methods=["post", "delete"], detail=True)
    def shopping_cart(self, request, pk):
        """Метод работает со списком покупок"""
        if request.method == "POST":
            if ShoppingCart.objects.filter(
                user=request.user, recipe__id=pk
            ).exists():
                return Response(
                    "Этот рецепт уже есть в вашем списке покупок",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            shopping_cart = ShoppingCart.objects.create(
                recipe_id=pk, user=request.user
            )
            if shopping_cart:
                return Response(
                    "Рецепт успешно добавлен в список покупок",
                    status=status.HTTP_201_CREATED,
                )

        if request.method == "DELETE":
            shopping_cart = ShoppingCart.objects.filter(
                user=request.user, recipe__id=pk
            )
            if shopping_cart:
                shopping_cart.delete()
                return Response(
                    "Рецепт успешно удален из списка покупок",
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                "Этот рецепт уже удален",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return None

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, pk):
        """Метод работает со списком избранных рецептов"""
        if request.method == "POST":
            if Favorite.objects.filter(
                user=request.user, recipe__id=pk
            ).exists():
                return Response(
                    "Этот рецепт уже в избранном",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            favorite = Favorite.objects.create(recipe_id=pk, user=request.user)
            if favorite:
                return Response(
                    "Рецепт успешно добавлен в избранное",
                    status=status.HTTP_201_CREATED,
                )

        if request.method == "DELETE":
            favorite = Favorite.objects.filter(
                user=request.user, recipe__id=pk
            )
            if favorite:
                favorite.delete()
                return Response(
                    "Рецепт успешно удален из избранного",
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                "Этот рецепт уже удален из избранного",
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response()

    @action(methods=["get"], detail=False)
    def download_shopping_cart(self, request):
        list_ingredient = (
            request.user.shopping_cart.all()
            .values_list(
                "recipe__recipe_to_ingredient__ingredient",
            )
            .annotate(amount=Sum("recipe__recipe_to_ingredient__amount"))
        )

        file = open("text.txt", "w")

        for ingredient in list_ingredient:
            ingredient_obj = get_object_or_404(Ingredient, id=ingredient[0])
            output_string = (
                f"{ingredient_obj.name}"
                f" {ingredient[1]}"
                f"({ingredient_obj.measurement_unit})"
            )
            file.write(output_string + "\n")
        file.close()

        with open("text.txt", "rb") as file:
            response = HttpResponse(
                file.read(), content_type="text/plain," " charset=utf8"
            )
            response[
                "Content-Disposition"
            ] = f'attachment; filename="Список покупок.txt"'

        return response


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (AllowAny,)
    pagination_class = None


class AmountIngredientViewSet(viewsets.ModelViewSet):
    queryset = AmountIngredient.objects.all()
    serializer_class = AmountIngredientSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        subscriptions = Subscription.objects.values("author_id").filter(
            subscriber=self.request.user
        )
        queryset = User.objects.filter(id__in=subscriptions)
        return queryset


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscribeSerializer

    @action(methods=["post", "delete"], detail=True)
    def subscribe(self, request, pk):
        """Метод работает с подпиской"""
        if request.method == "POST":
            if Subscription.objects.filter(
                subscriber=request.user, author__id=pk
            ).exists():
                return Response(
                    "Вы подписаны на этого автора",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            subscribe = Subscription.objects.create(
                author_id=pk, subscriber=request.user
            )
            if subscribe:
                return Response(
                    "Вы подписались",
                    status=status.HTTP_201_CREATED,
                )

        if request.method == "DELETE":
            subscribe = Subscription.objects.filter(
                subscriber=request.user, author__id=pk
            )
            if subscribe:
                subscribe.delete()
                return Response(
                    "Успешная отписка",
                    status=status.HTTP_204_NO_CONTENT,
                )

            return Response(
                "Вы не подписаны",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response()
