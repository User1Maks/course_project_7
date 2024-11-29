from datetime import time

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from habits.models import Habit
from habits.validators import validate_time_to_complete


class HabitSerializers(serializers.ModelSerializer):
    """Serializer для модели привычек."""

    time_to_complete = serializers.CharField(
        validators=[validate_time_to_complete],
        required=False
    )
    periodicity = serializers.IntegerField(
        min_value=1,
        max_value=7,
        required=False
    )

    def validate(self, data):
        """Валидация данных."""

        if data.get('related_habit') and data.get('reward'):
            raise ValidationError(
                "Нельзя одновременно заполнять поля вознаграждения "
                "и связанной привычки. Можно заполнить только одно"
                "из двух."
            )
        # Полезные привычки
        if not data.get('is_pleasant'):
            if not (data.get('related_habit') or data.get('reward')):
                raise ValidationError(
                    "Выберите приятную привычку или вознаграждение."
                )

        # Приятные привычки
        if data.get('is_pleasant'):
            if data.get('related_habit') or data.get('reward'):
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения "
                    "или связанной привычки."
                )

        if data.get('time_to_complete') is None:
            data['time_to_complete'] = time(0, 2)
            return data

        if (data.get('related_habit') and
                not data.get('related_habit').is_pleasant):
            raise ValidationError(
                "В связанные привычки могут попадать только привычки с "
                "признаком приятной привычки."
            )

        return data

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ('owner', 'next_day',)
        extra_kwargs = {'owner': {'required': False}}
