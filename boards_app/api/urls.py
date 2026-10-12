from django.urls import path

from .views import BoardViewSet


app_name = "boards_app"

urlpatterns = [
    path(
        "boards/",
        BoardViewSet.as_view({"post": "create"}),
        name="board-list",
    ),
]