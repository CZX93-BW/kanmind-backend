from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from auth_app.api.serializers import UserSerializer
from boards_app.models import Board
from tasks_app.models import Task


User = get_user_model()


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


class TaskSerializer(BoardTaskSerializer):
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
        board = (
            self.instance.board
            if self.instance is not None
            else attrs["board"]
        )
        for field in ("assignee", "reviewer"):
            if field in attrs:
                self.validate_membership(board, attrs[field], field)
        return attrs

    def validate_membership(self, board, user, field):
        if user is None:
            return
        if not board.members.filter(pk=user.pk).exists():
            raise serializers.ValidationError({
                f"{field}_id": "The user must be a member of this board."
            })