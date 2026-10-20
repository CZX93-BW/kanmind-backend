"""Validate board input and serialize board responses."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from auth_app.api.serializers import UserSerializer
from boards_app.models import Board
from tasks_app.api.serializers import BoardTaskSerializer


User = get_user_model()


class BoardWriteSerializer(serializers.ModelSerializer):
    """Validate board titles and member IDs for write operations."""

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Board
        fields = ("title", "members")


class BoardSummarySerializer(serializers.ModelSerializer):
    """Expose board metadata and counts annotated by the queryset."""

    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    owner_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Board
        fields = (
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        )
        read_only_fields = fields


class BoardDetailSerializer(serializers.ModelSerializer):
    """Expose board details with nested member and task information."""

    owner_id = serializers.IntegerField(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    tasks = BoardTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ("id", "title", "owner_id", "members", "tasks")
        read_only_fields = fields


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    """Return the updated board with nested owner and member data."""

    owner_data = UserSerializer(source="owner", read_only=True)
    members_data = UserSerializer(
        source="members",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Board
        fields = ("id", "title", "owner_data", "members_data")
        read_only_fields = fields