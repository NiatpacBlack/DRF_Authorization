from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

        """Пароль мы не возвращаем, поэтому устанавливаем ему значение только для записи."""
        extra_kwargs = {
            'password': {"write_only": True},
        }

    def create(self, validated_data):
        """Функция, которая будет хэшировать наш пароль."""

        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
