from django.contrib import admin
from core.models import RankingEntry


@admin.register(RankingEntry)
class RankingEntryAdmin(admin.ModelAdmin):
    list_display = ['paper', 'score', 'last_recommended_at']
    list_filter = ['last_recommended_at']
    search_fields = ['paper__title']
