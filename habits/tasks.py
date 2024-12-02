from celery import shared_task
from config import settings
import requests
from habits.models import Habit
from requests.exceptions import RequestException


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

    try:
        response = requests.get(f'{settings.TELEGRAM_URL}'
                                f'{settings.TELEGRAM_TOKEN}/sendMessage',
                                params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        # обработка полученных данных
        print(f'Сообщение успешно отправлено: {data}')
    except RequestException as e:
        # обработка исключения
        print(f'Ошибка отправки сообщения: {e}')

    # apply_async - для асинхронного выполнения задачи с отложенным временем
    send_a_habit_reminder.apply_async((habit_id, chat_id), eta=habit.next_day)
