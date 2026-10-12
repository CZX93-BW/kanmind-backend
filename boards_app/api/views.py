from django.db import transaction
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from boards_app.models import Board
from tasks_app.models import Task

from .serializers import BoardSummarySerializer, BoardWriteSerializer


class BoardViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardWriteSerializer
    http_method_names = ["post", "options"]

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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        board = self.get_queryset().get(pk=serializer.instance.pk)
        response_data = BoardSummarySerializer(board).data
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)