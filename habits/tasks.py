from celery import shared_task
from config import settings
from django.core.mail import send_mail
import datetime

from habits.models import Habit


@shared_task
def send_a_habit_reminder(habit_id):
    """Отправляет напоминание о привычке. """
    # Текущая дата и время
    now = datetime.datetime.now()

    habit = Habit.objects.get(id=habit_id)
    name_habit = ''

    if habit.is_pleasant:
        name_habit = 'Приятная'
    else:
        name_habit = 'Полезная'

    if now > habit.start_day and habit.time_habit:

        send_mail(f'{name_habit} привычка.',
                  f'Напоминаю Вам о вашей привычке',
                  settings.EMAIL_HOST_USER,
                  [habit.user]
                  )
