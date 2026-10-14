from django.urls import path

from .views import TaskViewSet


app_name = "tasks_app"

urlpatterns = [
    path(
        "tasks/",
        TaskViewSet.as_view({"post": "create"}),
        name="task-list",
    ),
]