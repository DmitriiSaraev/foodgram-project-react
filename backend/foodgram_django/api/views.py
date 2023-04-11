from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import UserSerializer, RecipeSerializer
from recipes.models import Recipe
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer



# Получить конкретные записи без кверисета,
# нужно переопределить метод get_quriset
# Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 8/15

