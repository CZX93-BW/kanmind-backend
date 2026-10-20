"""Define object-level access rules for tasks and comments."""

from rest_framework.permissions import BasePermission


class IsTaskBoardMember(BasePermission):
    """Allow task access to members of the associated board."""

    message = "You must be a member of this board."

    def has_object_permission(self, request, view, obj):
        """Check whether the user belongs to the task's board."""
        return obj.board.members.filter(pk=request.user.pk).exists()


class IsTaskCreatorOrBoardOwner(BasePermission):
    """Allow task access to its creator or its board owner."""

    message = "Only the task creator or board owner can delete this task."

    def has_object_permission(self, request, view, obj):
        """Check task creation or board ownership by the user."""
        return (
            obj.created_by_id == request.user.pk
            or obj.board.owner_id == request.user.pk
        )


class IsCommentAuthor(BasePermission):
    """Allow comment access only to its author."""

    message = "Only the comment author can delete this comment."

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user wrote the comment."""
        return obj.author_id == request.user.pk