from django.contrib import admin
from core.models import ReadingSession


@admin.register(ReadingSession)
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = ['paper', 'date', 'duration_minutes', 'created_at']
    list_filter = ['date', 'created_at']
    search_fields = ['paper__title', 'quick_notes']
