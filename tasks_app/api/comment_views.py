"""Provide task comment creation, listing and author-only deletion."""

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks_app.models import Comment, Task

from .comment_serializers import CommentSerializer
from .permissions import IsCommentAuthor, IsTaskBoardMember


class CommentListCreateView(ListCreateAPIView):
    """Allow board members to read and create comments on a task."""

    queryset = Comment.objects.select_related("author").order_by(
        "created_at", "id"
    )
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsTaskBoardMember]
    pagination_class = None
    http_method_names = ["get", "post", "head", "options"]

    def get_task(self):
        """Find the task and verify the requesting user's membership."""
        queryset = Task.objects.select_related("board")
        task = get_object_or_404(queryset, pk=self.kwargs["task_id"])
        self.check_object_permissions(self.request, task)
        return task

    def get_queryset(self):
        """Return ordered comments belonging to the accessible task."""
        task = self.get_task()
        return super().get_queryset().filter(task=task)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Create a comment authored by the authenticated user."""
        task = self.get_task()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(DestroyAPIView):
    """Allow authors to delete comments through the matching task."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = "comment_id"
    http_method_names = ["delete", "options"]

    def get_object(self):
        """Validate both URL IDs before looking up the comment."""
        for field in ("task_id", "comment_id"):
            value = self.kwargs[field]
            if not value.isascii() or not value.isdecimal():
                raise ValidationError({
                    field: "A valid integer is required."
                })
        return super().get_object()

    def get_queryset(self):
        """Restrict comment lookup to the task specified in the URL."""
        return super().get_queryset().filter(
            task_id=self.kwargs["task_id"]
        )