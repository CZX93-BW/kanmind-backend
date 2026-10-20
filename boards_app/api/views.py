"""Provide board operations with access checks and task statistics."""

from django.db import transaction
from django.db.models import Count, Prefetch, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from boards_app.models import Board
from tasks_app.models import Task

from .permissions import IsBoardOwner, IsBoardOwnerOrMember
from .serializers import (
    BoardDetailSerializer,
    BoardSummarySerializer,
    BoardUpdateResponseSerializer,
    BoardWriteSerializer,
)


class BoardViewSet(ModelViewSet):
    """Manage boards with action-specific access and responses."""

    permission_classes = [IsAuthenticated, IsBoardOwnerOrMember]
    serializer_class = BoardWriteSerializer
    pagination_class = None
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
        "head",
        "options",
    ]

    queryset = Board.objects.annotate(
        member_count=Count("members", distinct=True),
        ticket_count=Count("tasks", distinct=True),
        tasks_to_do_count=Count(
            "tasks",
            filter=Q(tasks__status=Task.Status.TO_DO),
            distinct=True,
        ),
        tasks_high_prio_count=Count(
            "tasks",
            filter=Q(tasks__priority=Task.Priority.HIGH),
            distinct=True,
        ),
    ).order_by("id")

    def get_permissions(self):
        """Select owner-only deletion or owner/member access checks."""
        if self.action == "destroy":
            return [IsAuthenticated(), IsBoardOwner()]
        return super().get_permissions()

    def get_queryset(self):
        """Filter accessible boards and load related detail data."""
        queryset = super().get_queryset()
        if self.action == "list":
            user = self.request.user
            return queryset.filter(
                Q(owner=user) | Q(members=user)
            ).distinct()
        if self.action == "retrieve":
            return self.get_detail_queryset()
        return queryset

    def get_detail_queryset(self):
        """Load members and tasks with users and comment counts."""
        tasks = Task.objects.select_related("assignee", "reviewer")
        tasks = tasks.annotate(comments_count=Count("comments")).order_by("id")
        return Board.objects.prefetch_related(
            "members",
            Prefetch("tasks", queryset=tasks),
        )

    def get_serializer_class(self):
        """Select the serializer for the current board action."""
        if self.action == "list":
            return BoardSummarySerializer
        if self.action == "retrieve":
            return BoardDetailSerializer
        return BoardWriteSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a board and return its summary with counts."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        board = self.get_queryset().get(pk=serializer.instance.pk)
        response_data = BoardSummarySerializer(board).data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        """Assign the authenticated user as the new board's owner."""
        serializer.save(owner=self.request.user)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        """Update fields and return nested owner and member data."""
        board = self.get_object()
        serializer = self.get_serializer(
            board, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = BoardUpdateResponseSerializer(serializer.instance).data
        return Response(response_data, status=status.HTTP_200_OK)