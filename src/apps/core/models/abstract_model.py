import uuid as uuid
from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _


class AbstractModelManager(models.Manager):
    """
    Менеджер абстрактной модели
    """
    def get_queryset(self):
        return super(AbstractModelManager, self).get_queryset().exclude(is_deleted=True)


class AbstractModel(models.Model):
    """
    Абстрактная модель
    """
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, verbose_name=_(u'UUID'))

    created_at = models.DateTimeField(default=timezone.now, verbose_name=_(u'Время создания'))

    is_deleted = models.BooleanField(default=False, verbose_name=_(u'Удалена'))
    objects = AbstractModelManager()

    class Meta:
        db_table = u'abstract'
        verbose_name = u'Абстрактная модель'
        verbose_name_plural = u'Абстрактные модели'
        abstract = True
