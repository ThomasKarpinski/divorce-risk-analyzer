from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'short_content', 'created_at')
    list_filter = ('role', 'created_at', 'user')
    search_fields = ('content', 'user__username')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content Preview'