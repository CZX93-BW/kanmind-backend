"""Define boards with an owner and independently assigned members."""

from django.conf import settings
from django.db import models


class Board(models.Model):
    """Represent a task board with an owner and optional members."""

    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_boards",
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="member_boards",
        blank=True,
    )

    def __str__(self):
        """Return the board title as its display label."""
        return self.title