from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from src.apps.core.models import AbstractModel, AbstractModelManager
from django.db import models
from typing import List


class UserManager(AbstractModelManager, BaseUserManager):
    """
    Менеджер создания
    """
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.save(using=self._db)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        user.user_permissions.set(Permission.objects.all())
        return user

    def get_users(self):
        return self.get_queryset().exclude(is_superuser=True)


class User(AbstractModel, AbstractUser):
    """
    Модель пользователя
    """
    MAX_LENGTH = 100
    first_name = models.CharField(default=u'Имя', max_length=MAX_LENGTH,
                                  blank=False, null=False, verbose_name=u'Имя')
    last_name = models.CharField(default=u'Фамилия', max_length=MAX_LENGTH,
                                 blank=False, null=False, verbose_name=u'Фамилия')
    middle_name = models.CharField(default='', max_length=MAX_LENGTH,
                                   blank=True, null=False, verbose_name=u'Отчество')

    email = models.EmailField(unique=True, null=False, max_length=MAX_LENGTH, verbose_name=u'Email пользователя')

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = u'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
        ordering = ['-created_at']
        permissions = (
            ('Редактирование пользователя', 'user_change'),
            ('Добавление пользователя', 'user_add'),
            ('Удаление пользователя', 'user_delete')
        )

    def __str__(self):
        result = self.last_name + ' ' + self.first_name
        if self.middle_name:
            result += ' ' + self.middle_name
        return result

    def save(self, *args, **kwargs):
        if self.username != self.email:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        return perm in get_user_permissions(self)

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        return app_label in get_user_module_permissions(self)

    def __eq__(self, other):
        if type(other) != User:
            return False
        return self.id == other.id


def get_user_permissions(user: User) -> List[str]:
    """
    Получает разрешения пользователя
    :param user: User
    :return: List[str]
    """
    permissions = list(map(
        lambda permission: permission.content_type.app_label + '.' + permission.codename,
        user.user_permissions.all()
    ))
    return permissions


def get_user_module_permissions(user: User) -> List[str]:
    """
    Получает список модулей в которых у пользователя есть разрешения
    :param user: User
    :return: List[str]
    """
    permissions = list(map(
        lambda perm: perm.content_type.app_label, user.user_permissions.all()
    ))
    return permissions
