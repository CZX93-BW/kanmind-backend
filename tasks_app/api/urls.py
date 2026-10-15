from django.urls import path

from .views import TaskViewSet


app_name = "tasks_app"

urlpatterns = [
    path(
        "tasks/",
        TaskViewSet.as_view({"post": "create"}),
        name="task-list",
    ),
    path(
        "tasks/assigned-to-me/",
        TaskViewSet.as_view({"get": "assigned_to_me"}),
        name="task-assigned-to-me",
    ),
    path(
        "tasks/reviewing/",
        TaskViewSet.as_view({"get": "reviewing"}),
        name="task-reviewing",
    ),
    path(
        "tasks/<int:pk>/",
        TaskViewSet.as_view({"patch": "partial_update"}),
        name="task-detail",
    ),
]