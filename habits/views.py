from datetime import timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.serializers import ValidationError
from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner, IsPublic
from habits.serializers import HabitSerializers
from habits.tasks import send_a_habit_reminder


class HabitCreateAPIView(generics.CreateAPIView):
    """ Habit create endpoint """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializers

    def perform_create(self, serializer):
        """Автоматически добавляет владельца привычки
        и день следующего выполнения привычки."""

        start_day = serializer.validated_data.get('start_day')

        if not start_day:
            raise ValidationError(
                'Дата и время для привычки должны быть указаны.')

        next_day = start_day

        habit = serializer.save(owner=self.request.user,
                                next_day=next_day)
        habit_id = habit.id
        # Запланировать первую задачу для отправки напоминания
        # Отправка напоминания будет выполнена асинхронно в будущем по
        # расписанию
        send_a_habit_reminder.apply_async(args=[habit_id],
                                          eta=next_day)


class HabitListAPIView(generics.ListAPIView):
    """ Habit list endpoint """

    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('is_pleasant', 'is_public',)
    ordering_fields = ('owner', 'start_day', 'next_day',)
    search_fields = ('owner',)
    pagination_class = HabitPaginator

    def get_queryset(self):
        """ Возвращает все привычки текущего пользователя """
        return Habit.objects.filter(owner=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """ Public habit list endpoint """
    serializer_class = HabitSerializers
    permission_classes = [IsOwner | IsPublic]

    def get_queryset(self):
        """ Возвращает все публичные привычки """
        return Habit.objects.filter(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """ Habit retrieve endpoint """

    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwner | IsPublic]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """ Habit update endpoint """

    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    permission_classes = [IsOwner]

    # def perform_update(self, serializer):
    #     """Автоматически обновляет день следующего выполнения привычки
    #             и пересылает напоминание, если необходимо."""
    #
    #     habit = self.get_object()
    #
    #     # Проверка наличия поля "start_day" в данных обновления
    #     start_day = serializer.validated_data.get('start_day', habit.start_day)
    #
    #     if not start_day:
    #         raise ValidationError(
    #             'Дата и время для привычки должны быть указаны.')
    #
    #     # Если периодичность была обновлена, пересчитываем следующий день
    #     periodicity = serializer.validated_data.get('periodicity',
    #                                                 habit.periodicity)
    #     next_day = start_day + timedelta(days=periodicity)
    #
    #     chat_id = self.request.user.tg_chat_id
    #
    #     # Сохраняем обновленные данные привычки
    #     habit = serializer.save(next_day=next_day)
    #
    #     # Запланировать задачу для отправки напоминания
    #     # Напоминание будет отправлено асинхронно в будущем
    #     send_a_habit_reminder.apply_async(args=[habit.id, chat_id],
    #                                       eta=habit.next_day)


class HabitDestroyAPIView(generics.DestroyAPIView):
    """ Habit delete endpoint """

    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
