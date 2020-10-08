from .abstract_model import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Log(AbstractModel):
    text = models.TextField(verbose_name=_(u'Текст'))

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='log_user',
                             verbose_name=_(u'Пользователь'))
    
    class Meta:
        db_table = u'logs'
        verbose_name = u'История действия'
        verbose_name_plural = u'История действий'
        ordering = ['-created_at']
