from rest_framework.permissions import BasePermission


class IsTaskBoardMember(BasePermission):
    message = "You must be a member of this board."

    def has_object_permission(self, request, view, obj):
        return obj.board.members.filter(pk=request.user.pk).exists()