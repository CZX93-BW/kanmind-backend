from django.db import transaction
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tasks_app.models import Task

from .serializers import TaskSerializer, TaskWriteSerializer


class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskWriteSerializer
    http_method_names = ["post", "options"]

    queryset = Task.objects.select_related(
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