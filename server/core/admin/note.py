from django.contrib import admin
from core.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'paper', 'note_type', 'created_at']
    list_filter = ['note_type', 'created_at']
    search_fields = ['title', 'content', 'paper__title']
