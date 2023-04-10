from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = User
        fields = (
            'email',
            'pk',
            'username',
            'first_name',
            'last_name',
            'password'
        )
