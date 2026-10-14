from django.db import transaction
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks_app.models import Task

from .permissions import IsTaskBoardMember
from .serializers import (
    TaskSerializer,
    TaskUpdateResponseSerializer,
    TaskWriteSerializer,
)


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsTaskBoardMember]
    serializer_class = TaskWriteSerializer
    http_method_names = ["post", "patch", "options"]
    queryset = Task.objects.select_related(
        "board",
        "assignee",
        "reviewer",
    ).annotate(
        comments_count=Count("comments"),
    ).order_by("id")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        task = self.get_queryset().get(pk=serializer.instance.pk)
        response_data = TaskSerializer(task).data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(
            task, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_data = TaskUpdateResponseSerializer(serializer.instance).data
        return Response(response_data, status=status.HTTP_200_OK)