"""Validate task input and serialize task responses."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from auth_app.api.serializers import UserSerializer
from boards_app.models import Board
from tasks_app.models import Task


User = get_user_model()


class BoardTaskSerializer(serializers.ModelSerializer):
    """Represent nested board tasks with users and comment counts."""

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


class TaskSerializer(BoardTaskSerializer):
    """Include board IDs in creation and personal list responses."""

    class Meta(BoardTaskSerializer.Meta):
        fields = (
            "id",
            "board",
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


class TaskUpdateResponseSerializer(BoardTaskSerializer):
    """Return updated task data without board ID or comment count."""

    class Meta(BoardTaskSerializer.Meta):
        fields = (
            "id",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
        )
        read_only_fields = fields


class TaskWriteSerializer(serializers.ModelSerializer):
    """Validate task fields, board access and user assignments."""

    board = serializers.IntegerField(min_value=1, write_only=True)
    assignee_id = serializers.PrimaryKeyRelatedField(
        source="assignee",
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Task
        fields = (
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee_id",
            "reviewer_id",
            "due_date",
        )

    def validate_board(self, value):
        """Prevent board changes and require board membership."""
        if self.instance is not None and value != self.instance.board_id:
            raise serializers.ValidationError(
                "The board of a task cannot be changed."
            )
        board = get_object_or_404(Board, pk=value)
        user = self.context["request"].user
        if not board.members.filter(pk=user.pk).exists():
            raise PermissionDenied("You must be a member of this board.")
        return board

    def validate(self, attrs):
        """Validate membership for new and retained assignments."""
        board = (
            self.instance.board
            if self.instance is not None
            else attrs["board"]
        )
        for field in ("assignee", "reviewer"):
            current_user = getattr(self.instance, field, None)
            user = attrs.get(field, current_user)
            self.validate_membership(board, user, field)
        return attrs

    def validate_membership(self, board, user, field):
        """Allow empty assignments or require board membership."""
        if user is None:
            return
        if not board.members.filter(pk=user.pk).exists():
            raise serializers.ValidationError({
                f"{field}_id": "The user must be a member of this board."
            })