from rest_framework import generics

from habits.models import Habit
from habits.serializers import HabitSerializers


class HabitCreateAPIView(generics.CreateAPIView):
    """Создание модели привычек."""

    serializer_class = HabitSerializers


class HabitListAPIView(generics.ListAPIView):
    """Получение списка всех привычек."""

    serializer_class = HabitSerializers
    queryset = Habit.objects.all()


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Получение информации об одной привычке."""

    serializer_class = HabitSerializers
    queryset = Habit.objects.all()


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Обновление информации о привычке."""

    serializer_class = HabitSerializers
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Удаление привычки."""

    queryset = Habit.objects.all()
