from rest_framework import serializers

from tasks_app.models import Comment


class CommentSerializer(serializers.ModelSerializer):
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