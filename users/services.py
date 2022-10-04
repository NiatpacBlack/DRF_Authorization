from .models import User


def get_user_where_email(email: str):
    """Возвращает QuerySet с тем пользователем email которого указан на вход."""

    return User.objects.filter(email=email).first()


def get_user_where_id(user_id: str):
    """Возвращает QuerySet с тем пользователем user_id которого указан на вход."""

    return User.objects.filter(id=user_id).first()
