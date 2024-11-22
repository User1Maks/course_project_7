from datetime import timedelta

from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Habit(models.Model):
    """Полезная привычка."""

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец привычки",
        related_name="habits",
    )
    place = models.CharField(
        max_length=255,
        verbose_name="Место привычки",
        help_text="Укажите место привычки",
        **NULLABLE,
    )
    time = models.TimeField(
        verbose_name="Время для привычки",
        help_text="Укажите время, когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие для привычки",
        help_text="Укажите действие для привычки",
    )
    start_day = models.DateTimeField(
        verbose_name="День начала выполнения привычки")
    next_day = models.DateTimeField(
        verbose_name="День следующей выполнения привычки", blank=True
    )

    # Признак приятной привычки
    is_pleasant = models.BooleanField(
        verbose_name="Приятная привычка",
        help_text="Укажите будет ли привычка приятной",
        default=False,
        blank=True,
    )

    # Связанная привычка (для полезных привычек)
    related_habit = models.ForeignKey(
        "habits.Habit",
        **NULLABLE,
        verbose_name="Связанная (приятная) привычка",
        on_delete=models.SET_NULL,
    )

    periodicity = models.PositiveSmallIntegerField(
        verbose_name="Периодичность привычки в днях",
        help_text="Укажите периодичность привычки в днях",
        default=1,
    )
    reward = models.CharField(
        max_length=255,
        verbose_name="Вознаграждение за привычку",
        help_text="Укажите вознаграждение за привычку",
        **NULLABLE,
    )

    time_to_complete = models.TimeField(
        verbose_name="Время на выполнение привычки",
        help_text="Укажите время на выполнение привычки (не более 2 мин)",
        default=timedelta(minutes=2),
        blank=True,
    )
    is_public = models.BooleanField(
        verbose_name="Публичность привычки",
        help_text="Укажите будет ли привычка публичной",
        default=False,
        blank=True,
    )

    def __str__(self):
        if self.place:
            return f"Я буду {self.action} в {self.time} в {self.place}."
        else:
            return f"Я буду {self.action} в {self.time}."

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
