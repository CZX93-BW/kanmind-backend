"""Define object-level access rules for boards."""

from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    """Allow board access to its owner or one of its members."""

    message = "You must be the board owner or a member."

    def has_object_permission(self, request, view, obj):
        """Check whether the user owns or belongs to the board."""
        if obj.owner_id == request.user.pk:
            return True
        return obj.members.filter(pk=request.user.pk).exists()


class IsBoardOwner(BasePermission):
    """Restrict board access to its owner."""

    message = "Only the board owner can delete this board."

    def has_object_permission(self, request, view, obj):
        """Check whether the requesting user owns the board."""
        return obj.owner_id == request.user.pk