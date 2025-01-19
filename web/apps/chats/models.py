from django.db import models
from django.utils.translation import gettext_lazy as _

from web.db.model_mixins import AsyncBaseModel


class Chat(AsyncBaseModel):
    """Модель telegram группы"""
    name = models.CharField(_('Название'), max_length=150)
    link = models.URLField(_('Ссылка на группу'), max_length=200)
    
    members = models.ManyToManyField(
        'telegram_users.TelegramUser',
        verbose_name=_('Учасники')
    )

    class Meta:
        verbose_name = _('Группа')
        verbose_name_plural = _('Группы')

    def __str__(self):
        return self.name


