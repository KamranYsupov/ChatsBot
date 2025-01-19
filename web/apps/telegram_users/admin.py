from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'telegram_id',
        'username', 
        'bot_link_status',
        'bot_start_link',
        'phone_number',
    )
    list_editable = (
        'phone_number',
    )
    
    search_fields = (
        'name__iregex',
        'username__iregex',
    )
    
    exclude = (
        'telegram_id',
        'username', 
        'bot_start_link',
        'bot_link_status',
    )
    
