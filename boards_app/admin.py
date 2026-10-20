"""Configure board management in Django Admin."""

from django.contrib import admin

from .models import Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """Display boards with owner search and member selection."""

    list_display = ("id", "title", "owner")
    search_fields = ("title", "owner__email")
    autocomplete_fields = ("owner",)
    filter_horizontal = ("members",)
    list_select_related = ("owner",)
    ordering = ("id",)