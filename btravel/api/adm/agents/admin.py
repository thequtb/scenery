from django.contrib import admin
from .models import Agent, Conversation, Message

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'agent', 'is_active', 'created_at')
    list_filter = ('is_active', 'agent')
    readonly_fields = ('id', 'collected_data')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'content', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('content',)
