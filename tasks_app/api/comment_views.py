from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tasks_app.models import Comment, Task

from .comment_serializers import CommentSerializer
from .permissions import IsCommentAuthor, IsTaskBoardMember


class CommentListCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsTaskBoardMember]
    pagination_class = None
    http_method_names = ["get", "post", "head", "options"]

    def get_task(self):
        queryset = Task.objects.select_related("board")
        task = get_object_or_404(queryset, pk=self.kwargs["task_id"])
        self.check_object_permissions(self.request, task)
        return task

    def get_queryset(self):
        task = self.get_task()
        return Comment.objects.filter(task=task).select_related(
            "author"
        ).order_by("created_at", "id")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        task = self.get_task()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(task=task, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    lookup_url_kwarg = "comment_id"
    http_method_names = ["delete", "options"]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs["task_id"])