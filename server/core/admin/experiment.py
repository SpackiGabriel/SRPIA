from django.contrib import admin
from core.models import Experiment


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'owner', 'created_at']
    list_filter = ['status', 'owner', 'created_at']
    search_fields = ['title', 'description']
    filter_horizontal = ['papers']
