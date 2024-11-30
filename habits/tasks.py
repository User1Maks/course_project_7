from celery import shared_task
from config import settings
import requests
from habits.models import Habit


@shared_task
def send_a_habit_reminder(habit_id, chat_id):
    """Функция для отправки напоминания о привычке."""
    habit = Habit.objects.get(id=habit_id)

    if habit.related_habit:
        message = (f'Напоминаю Вам о необходимости {habit.action} и '
                   f'{habit.related_habit.action}')
    else:
        message = (f'Напоминаю Вам о необходимости {habit.action} и '
                   f'вознаградите себя {habit.reward}')

    params = {
        'text': message,
        'chat_id': chat_id,
    }

    requests.get(f'{settings.TELEGRAM_URL}'
                 f'{settings.TELEGRAM_TOKEN}/sendMessage', params=params)

    # apply_async - для асинхронного выполнения задачи с отложенным временем
    send_a_habit_reminder.apply_async((habit_id, chat_id), eta=habit.next_day)
