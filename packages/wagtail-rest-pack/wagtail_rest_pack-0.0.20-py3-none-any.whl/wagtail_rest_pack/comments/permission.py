from rest_framework.permissions import BasePermission

from wagtail_rest_pack.comments.models import Comment


class CommentOwnerOrStaff(BasePermission):

    def has_object_permission(self, request, view, obj: Comment):
        user =request.user
        if user  is None:
            return False
        created_by = obj.created_by
        is_staff = user.is_staff or user.is_superuser
        if created_by is not None and created_by.id == user.id:
            return True
        return is_staff


