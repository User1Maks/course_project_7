from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from config import settings
import requests
from habits.models import Habit
from requests.exceptions import RequestException


@shared_task
def send_a_habit_reminder():
    """Функция для отправки напоминания о привычке."""

    current_datetime = timezone.now()

    habits = Habit.objects.all()

    for habit in habits:

        if habit.next_day.tzinfo is None:
            habit_next_day_aware = timezone.make_aware(habit.next_day)
        else:
            habit_next_day_aware = habit.next_day

        if (habit_next_day_aware.date() == current_datetime.date() and
                habit_next_day_aware.time() <= current_datetime.time()):
            periodicity = habit.periodicity
            habit.next_day = habit_next_day_aware + timedelta(days=periodicity)
            habit.save()
            chat_id = habit.owner.tg_chat_id

            # Формируем сообщение
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
                # Отправляем запрос в Telegram API
                response = requests.get(f'{settings.TELEGRAM_URL}'
                                        f'{settings.TELEGRAM_TOKEN}/sendMessage',
                                        params=params)
                response.raise_for_status()  # Проверка на ошибки HTTP
                data = response.json()
                print(f'Сообщение успешно отправлено: {data}')
            except RequestException as e:
                print(f'Ошибка отправки сообщения: {e}')


# @shared_task
# def send_a_habit_reminder(habit_id):
#     """Функция для отправки напоминания о привычке."""
#
#     habit_obj = Habit.objects.get(id=habit_id)
#
#     periodicity = habit_obj.periodicity
#     habit_obj.next_day = habit_obj.start_day + timedelta(days=periodicity)
#     habit_obj.save()
#     chat_id = habit_obj.owner.tg_chat_id
#
#     # Формируем сообщение
#     if habit_obj.related_habit:
#         message = (f'Напоминаю Вам о необходимости {habit_obj.action} и '
#                    f'{habit_obj.related_habit.action}')
#     else:
#         message = (f'Напоминаю Вам о необходимости {habit_obj.action} и '
#                    f'вознаградите себя {habit_obj.reward}')
#
#     params = {
#         'text': message,
#         'chat_id': chat_id,
#     }
#
#     try:
#         # Отправляем запрос в Telegram API
#         response = requests.get(f'{settings.TELEGRAM_URL}'
#                                 f'{settings.TELEGRAM_TOKEN}/sendMessage',
#                                 params=params)
#         response.raise_for_status()  # Проверка на ошибки HTTP
#         data = response.json()
#         print(f'Сообщение успешно отправлено: {data}')
#     except RequestException as e:
#         print(f'Ошибка отправки сообщения: {e}')
#
#     # apply_async - для асинхронного выполнения задачи с отложенным временем
#     send_a_habit_reminder.apply_async(args=[habit_obj.id],
#                                       eta=habit_obj.next_day)
