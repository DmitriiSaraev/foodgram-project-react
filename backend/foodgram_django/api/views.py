from rest_framework import viewsets

from api.serializers import UserSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# Получить конкретные записи без кверисета,
# нужно переопределить метод get_quriset
# Спринт 8/18 → Тема 1/3: Django Rest Framework → Урок 8/15

