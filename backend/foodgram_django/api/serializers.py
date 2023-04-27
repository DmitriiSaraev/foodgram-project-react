from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Recipe, Follow, Tag, Ingredient, AmountIngredient, \
    Favorite, RecipeTag
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
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return Favorite.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        return False

    def validate_tags(self, value):
        if len(value) == 0:
            raise serializers.ValidationError(
                'У рецепта должен быть минимум 1 тег!')

    def validate_user(self, value):
        pass

    def create(self, validated_data):
        print(validated_data)
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            current_tag = Tag.objects.get(**tag)
            RecipeTag.objects.create(
                tag=current_tag, recipe=recipe)

        return recipe

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
            'is_favorited'
        )
