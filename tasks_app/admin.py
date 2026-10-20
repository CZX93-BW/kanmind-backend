"""Configure task and comment management in Django Admin."""

from django.contrib import admin

from .models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Display tasks with workflow filters and user selection."""

    list_display = (
        "id",
        "title",
        "board",
        "status",
        "priority",
        "assignee",
        "reviewer",
        "due_date",
    )
    list_filter = ("status", "priority")
    search_fields = ("title", "description", "board__title")
    autocomplete_fields = ("board", "assignee", "reviewer", "created_by")
    list_select_related = ("board", "assignee", "reviewer")
    ordering = ("id",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Display comments with author search and a read-only timestamp."""

    list_display = ("id", "task", "author", "created_at")
    search_fields = ("content", "task__title", "author__email")
    autocomplete_fields = ("task", "author")
    readonly_fields = ("created_at",)
    list_select_related = ("task", "author")
    ordering = ("created_at", "id")