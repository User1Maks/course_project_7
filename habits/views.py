from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.serializers import ValidationError
from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner, IsPublic
from habits.serializers import HabitSerializers


class HabitCreateAPIView(generics.CreateAPIView):
    """ Habit create endpoint """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializers

    def perform_create(self, serializer):
        """Автоматически добавляет владельца привычки
        и день следующего выполнения привычки."""

        start_day = serializer.validated_data.get('start_day')
        habit_time = serializer.validated_data.get('time_habit')

        if not (start_day and habit_time):
            raise ValidationError(
                'Дата и время для привычки должны быть указаны.')

        # Устанавливаем день и время выбранное пользователем
        start_day_with_time = datetime.combine(start_day, habit_time)
        periodicity = serializer.validated_data.get('periodicity', 1)
        next_day = start_day + timedelta(days=periodicity)

        habit = serializer.save(owner=self.request.user,
                                start_day=start_day_with_time,
                                next_day=next_day)
        habit.save()


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
    permission_classes = [IsOwner, IsPublic]

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


class HabitDestroyAPIView(generics.DestroyAPIView):
    """ Habit delete endpoint """

    queryset = Habit.objects.all()
    permission_classes = [IsOwner]
