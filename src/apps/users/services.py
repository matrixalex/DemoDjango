from typing import Union, Optional, NamedTuple
from .models import User
from django.contrib.auth import authenticate as auth, login

from ..core.errors import ErrorMessages


class UserAuthData(NamedTuple):
    status: bool
    message: str
    user: Optional[User]


def get_user_by_unique_field(user_id: Union[str, int] = None, email: str = None) -> Optional[User]:
    """
    Получить пользователя по id или email
    :param user_id: str, int
    :param email: str
    :return: User, None
    """
    try:
        if user_id:
            user = User.objects.get(pk=user_id)
            return user
        if email:
            user = User.objects.get(email=email)
            return user
    except User.DoesNotExist:
        return None


def authenticate(request, email: str, password: str) -> UserAuthData:
    """
    Авторизирует пользователя в системе
    :param request: request
    :param email: str
    :param password: str
    :return: UserAuthData = NamedTuple(status: bool, message: str, user: Optional[User]
    """
    user = auth(request, email=email, password=password)
    if not user:
        return UserAuthData(status=False, message=ErrorMessages.WRONG_EMAIL_OR_PASSWORD, user=None)
    login(request, user)
    return UserAuthData(status=True, message='', user=user)
