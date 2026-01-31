from rest_framework import permissions

class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешает:
    - GET/HEAD/OPTIONS — всем пользователям (безопасные методы).
    - PUT/PATCH/DELETE — только автору объекта или пользователям из группы «Модераторы».


    Требования:
    - Объект должен иметь поле `author` (ForeignKey на User).
    - Группа «Модераторы» должна существовать в БД.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not hasattr(obj, 'author'):
            return False

        is_owner = obj.author == request.user
        is_moderator = request.user.groups.filter(name='Модераторы').exists()


        return is_owner or is_moderator

    def has_permission(self, request, view):
        """
        Дополнительная проверка для действий, не связанных с конкретным объектом
        (например, создание объекта).
        """
        if view.action == 'create':
            return request.user.is_authenticated
        return True
