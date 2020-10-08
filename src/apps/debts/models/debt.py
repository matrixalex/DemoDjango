from django.db.models import Q
from src.apps.core.models import AbstractModel, AbstractModelManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class DebtManager(AbstractModelManager):
    def filter_by_user(self, user):
        """
        Фильтрует долги по пользователю
        :param user: User
        :return: QuerySet
        """
        debts = self.get_queryset().filter(Q(user=user) | Q(to_user=user))
        return debts


class Debt(AbstractModel):
    """
    Модель долга
    """
    text = models.TextField(verbose_name=_(u'Описание'), blank=True)

    price = models.PositiveIntegerField(verbose_name=_(u'Сумма'))

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='debt_user',
                             blank=True, null=True, verbose_name=_(u'Должник'))

    to_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='debt_to_user',
                                blank=True, null=True, verbose_name=_(u'Кредитор'))

    objects = DebtManager()

    class Meta:
        db_table = 'debts'
        verbose_name = _('Долг')
        verbose_name_plural = _('Долги')
        ordering = ['-created_at']

    def __str__(self):
        return 'Долг ' + str(self.user) + ' пользователю ' + str(self.to_user)
