from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Разрешает доступ пользователям из группы 'moderators'."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='moderators').exists()
        )

class IsOwnerOrModerator(permissions.BasePermission):
    """Разрешает доступ владельцу объекта или модератору."""
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='moderators').exists():
            return True
        return obj == request.user
