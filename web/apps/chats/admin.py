from django.contrib import admin

from .models import Chat


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'name', 
        'link', 
    )
    
    filter_horizontal = ('members', )
    
