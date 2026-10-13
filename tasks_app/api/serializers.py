from rest_framework import serializers

from auth_app.api.serializers import UserSerializer
from tasks_app.models import Task


class BoardTaskSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True, allow_null=True)
    reviewer = UserSerializer(read_only=True, allow_null=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count",
        )
        read_only_fields = fields