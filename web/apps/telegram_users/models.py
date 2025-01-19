from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from web.db.model_mixins import (
    AsyncBaseModel,
    AbstractTelegramUser,
)


class TelegramUser(AbstractTelegramUser):
    """Модель telegram пользователя"""
    
    class BotLinkStatus:
        NOT_ACTIVATED = 'NOT_ACTIVATED'
        ACTIVATED = 'ACTIVATED'
        
        CHOICES = (
            (NOT_ACTIVATED, _('Не активирована')),
            (ACTIVATED, _('Активирована')),
        ) 
    
    name = models.CharField(
        _('Имя'),
        max_length=150
    )
    phone_number = models.CharField(
        _('Номер телефона'),
        max_length=50,
        unique=True,
    )
    bot_start_link = models.CharField(
        _('Ссылка для запуска бота'),
        max_length=150,
        unique=True,
        editable=False,
    )
    bot_link_status = models.CharField(
        _('Статус ссылки'),
        choices=BotLinkStatus.CHOICES,
        default=BotLinkStatus.NOT_ACTIVATED,
        max_length=50
    )

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('Telegram пользователи')

    def __str__(self):
        return f'{self.name} {self.phone_number}'
    
    def save(self, *args, **kwargs):
        if self._state.adding: # Если создаем объект 
            self.bot_start_link = f'{settings.BOT_LINK}?start={self.id}'
            
        return super().save(*args, **kwargs)
