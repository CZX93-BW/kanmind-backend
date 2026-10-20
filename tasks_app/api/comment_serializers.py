"""Serialize task comments and validate their content."""

from rest_framework import serializers

from tasks_app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """Expose comment content, timestamp and the author's full name."""

    author = serializers.CharField(
        source="author.fullname",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "created_at",
            "author",
            "content",
        )
        read_only_fields = (
            "id",
            "created_at",
            "author",
        )