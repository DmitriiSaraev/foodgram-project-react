from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import Recipe, Subscription, Tag, Ingredient, AmountIngredient, \
    Favorite, RecipeTag, ShoppingCart
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
            return Subscription.objects.filter(
                subscriber=self.context['request'].user,
                author=obj).exists()
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
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    # def to_representation(self, instance):
    #     # Добавляем отладочный вывод
    #     return super().to_representation(instance)

    class Meta:
        model = AmountIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    # Про картинки Спринт 9/18 → Тема 2/4: Взаимодействие фронтенда и
    # бэкенда → Урок 1/7
    author = UserSerializer(
            read_only=True, default=serializers.CurrentUserDefault())
    tags = TagSerializer(many=True, read_only=True)
    ingredients = AmountIngredientSerializer(
        many=True,
        read_only=True,
        source='recipe_to_ingredient'
    )
    is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    # author = serializers.PrimaryKeyRelatedField(
    #     read_only=True, default=serializers.CurrentUserDefault())

    def to_representation(self, instance):
        # Добавляем отладочный вывод
        print(instance)
        return super().to_representation(instance)


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

    def get_tags(self):
        # if self.context.get('request').data.get('tags'):
        tags_id = self.context.get('request').data.get('tags')
        tags = Tag.objects.filter(id__in=tags_id)
        if tags:
            return tags
        raise serializers.ValidationError(
            'У рецепта должен быть минимум 1 тег!')

    def get_ingredients(self, dict):
        ingredients_id = []
        ingredients_amount = []
        ingredients_raw = self.context.get('request').data.get('ingredients')
        for value in ingredients_raw:
            ingredients_id.append(value.get('id'))
            ingredients_amount.append(value.get('amount'))
        ingredients = Ingredient.objects.filter(id__in=ingredients_id)
        return ingredients

    def create(self, validated_data):
        # tags_id = self.context.get('request').data.get('tags')
        # tags = Tag.objects.filter(id__in=tags_id)
        tags = self.get_tags()
        ingredients = self.initial_data.get('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            RecipeTag.objects.create(
                tag=tag, recipe=recipe)

        for ingredient in ingredients:
            AmountIngredient.objects.create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(pk=ingredient.get('id')),
                amount=ingredient.get('amount'))

        return recipe

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
            'is_favorited'
        )
        read_only_fields = ('author',)


class ShopingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe',
        )


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    '''Для отображения рецептов в подписке'''
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'cooking_time',
        )


class SubscriptionsSerializer(serializers.ModelSerializer):
    '''Поулучает подписки'''
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    is_subscribed = serializers.SerializerMethodField()
    recipes = SubscriptionsRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()




class SubscribeSerializer(serializers.ModelSerializer):
    '''Подписывается'''
    author = UserSerializer(
            read_only=True, default=serializers.CurrentUserDefault())


    class Meta:
        model = Subscription
        fields = (
            'author',
            'subscriber',
        )


