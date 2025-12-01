from django.contrib import admin
from core.models import Paper


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'status', 'progress_percent', 'owner', 'created_at']
    list_filter = ['priority', 'status', 'owner', 'created_at']
    search_fields = ['title', 'abstract', 'authors__name']
    filter_horizontal = ['authors', 'tags']
    readonly_fields = ['created_at', 'updated_at']
