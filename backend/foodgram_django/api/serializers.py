from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Recipe, Follow, Tag, Ingredient, AmountIngredient, \
    Favorite
from users.models import User
from djoser.serializers import UserCreateSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return Follow.objects.filter(
                follower=self.context['request'].user,
                following=obj).exists()
        return False


class CastomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            'id',
            "username",
            "first_name",
            "last_name",
            "password",
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class AmountIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmountIngredient
        fields = (
            'id',
            'ingredient',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    # Про картинки Спринт 9/18 → Тема 2/4: Взаимодействие фронтенда и
    # бэкенда → Урок 1/7
    author = UserSerializer()
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return Favorite.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        return False

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
            'is_favorited'
        )
