from rest_framework.permissions import BasePermission


class IsBoardOwnerOrMember(BasePermission):
    message = "You must be the board owner or a member."

    def has_object_permission(self, request, view, obj):
        if obj.owner_id == request.user.pk:
            return True
        return obj.members.filter(pk=request.user.pk).exists()


class IsBoardOwner(BasePermission):
    message = "Only the board owner can delete this board."

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.pk