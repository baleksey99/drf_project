from rest_framework import permissions

class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешает:
    - Всем: чтение (GET, HEAD, OPTIONS).
    - Автору объекта или модератору: редактирование (PUT/PATCH) и удаление (DELETE).
    """

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = obj.author == request.user
        is_moderator = request.user.groups.filter(name='Модераторы').exists()


        return is_owner or is_moderator
