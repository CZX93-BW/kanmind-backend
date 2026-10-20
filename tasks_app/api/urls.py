from django.urls import path

from .comment_views import CommentDeleteView, CommentListCreateView
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
        "tasks/<int:task_id>/comments/",
        CommentListCreateView.as_view(),
        name="task-comments",
    ),
    path(
        "tasks/<str:task_id>/comments/<str:comment_id>/",
        CommentDeleteView.as_view(),
        name="task-comment-detail",
    ),
    path(
        "tasks/<str:pk>/",
        TaskViewSet.as_view({
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="task-detail",
    ),
]