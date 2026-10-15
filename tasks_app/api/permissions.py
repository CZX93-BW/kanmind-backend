from rest_framework.permissions import BasePermission


class IsTaskBoardMember(BasePermission):
    message = "You must be a member of this board."

    def has_object_permission(self, request, view, obj):
        return obj.board.members.filter(pk=request.user.pk).exists()


class IsTaskCreatorOrBoardOwner(BasePermission):
    message = "Only the task creator or board owner can delete this task."

    def has_object_permission(self, request, view, obj):
        return (
            obj.created_by_id == request.user.pk
            or obj.board.owner_id == request.user.pk
        )