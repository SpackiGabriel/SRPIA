from django.contrib import admin
from core.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'affiliation']
    search_fields = ['name', 'affiliation']
