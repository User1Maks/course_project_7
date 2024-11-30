from rest_framework.permissions import BasePermission

from habits.models import Habit


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_permission(self, request, view):
        """Проверяем пользователя на принадлежность к владельцу объекта"""
        if request.user and view.kwargs.get('pk'):
            habit = Habit.objects.get(id=view.kwargs.get('pk'))
            return request.user == habit.owner
        return False


class IsPublic(BasePermission):
    """Проверяет, является ли объект публичным."""

    def has_object_permission(self, request, view, obj):
        return obj.is_public
