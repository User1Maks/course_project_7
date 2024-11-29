from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_permission(self, request, view):
        """Проверяем пользователя на принадлежность к владельцу объекта"""

        return request.user == view.get_object().owner


class IsPublic(BasePermission):
    """Проверяет, является ли объект публичным."""

    def has_object_permission(self, request, view, obj):
        return obj.is_public
