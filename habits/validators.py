from datetime import timedelta

from rest_framework.serializers import ValidationError


def validate_time_to_complete(time_to_complete):
    """
    Валидатор для проверки времени выполнения привычки, оно не
    должно превышать 2 минут.
    """
    try:
        time_to_complete = time_to_complete.split(':')
        if len(time_to_complete) != 2:
            raise ValidationError(
                'Время выполнения должно быть указано в формате MM:SS. '
                'Например 01:40')
        minute = time_to_complete[0]
        second = time_to_complete[1]
        time_to_complete = timedelta(minutes=int(minute), seconds=int(second))

    except TypeError as e:
        raise ValidationError(e)

    if time_to_complete > timedelta(seconds=120):
        raise ValidationError(
            "Время выполнения должно быть превышать 120 секунд."
        )
