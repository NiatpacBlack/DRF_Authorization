import datetime

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import UserSerializer
from users.services import get_user_where_email, get_user_where_id


class RegistrationView(APIView):
    """APi представление регистрации."""

    def post(self, request):
        """
        Принимает запрос с данными пользователя для регистрации, передает их в сериалайзер.

        Данные сохраняются в модели и возвращается json ответ от сервера.
        """
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    """Api представление авторизации."""

    def post(self, request):
        """Возвращает пользователя. Если уникальный email есть в модели, и пароль присутствует."""

        email = request.data['email']
        password = request.data['password']
        user = get_user_where_email(email=email)

        if user is None:
            raise AuthenticationFailed('Пользователь на найден')
        if not user.check_password(password):
            raise AuthenticationFailed('Неверный пароль')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=300),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm="HS256")

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
        }

        return response


class UserView(APIView):
    """Api представление данных о пользователе."""

    def get(self, request):
        """Получает cookie файл, и достает оттуда token, чтобы получить данные о пользователе."""

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Не пройдена проверка подлинности')

        """Декодируем jwt токен доставая оттуда информацию алгоритмом. Если токен истек, рейзим ошибку."""
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Токен авторизации истек')

        user = get_user_where_id(user_id=payload['id'])
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    """Api представление выхода их системы."""

    def post(self, request):
        """При получении запроса удаляем cookie файл c jwt токеном. И возвращаем ответ об успехе."""

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Успешно',
        }

        return response
