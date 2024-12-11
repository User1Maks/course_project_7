from rest_framework.test import APITestCase
from django.urls import reverse

from habits.models import Habit
from users.models import User
from rest_framework import status


class HabitsTestCase(APITestCase):
    """Класс тестирования модели привычек."""

    def setUp(self):
        Habit.objects.all().delete()
        self.user = User.objects.create(username='Username',
                                        email='user@email.com')
        # авторизуем пользователя
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            owner=self.user,
            place='Локально',
            action='Test',
            start_day='2024-12-02T20:00:00+03:00',
            next_day='2024-12-02T20:00:00+03:00',
            periodicity=1,
            reward='Вознаграждение',
            time_to_complete='02:00'
        )

    def test_create_habits(self):
        """Тестирование создания привычек."""
        url = reverse('habits:habits-create')

        # Создание полезной привычки с вознаграждением
        data_1 = {
            'place': 'Локально',
            'action': 'Test',
            'start_day': '2024-12-02T20:00:00+03:00',
            'next_day': '2024-12-02T20:00:00+03:00',
            'reward': 'Вознаграждение 1',
            'time_to_complete': '02:00'
        }

        response_1 = self.client.post(url, data_1)

        # Проверка статуса ответа
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response_1.json(), {
                'id': 2,
                'place': 'Локально',
                'related_habit': None,
                'action': 'Test',
                'start_day': '2024-12-02T20:00:00+03:00',
                'next_day': '2024-12-02T20:00:00+03:00',
                'owner': 1,
                'is_pleasant': False,
                'periodicity': 1,
                'reward': 'Вознаграждение 1',
                'time_to_complete': '02:00',
                'is_public': False
            }
        )

        self.assertEqual(Habit.objects.all().count(), 2)

        # Создание приятной привычки
        data_2 = {
            'place': 'Локально',
            'action': 'Приятная привычка',
            'start_day': '2024-12-02T20:00:00+03:00',
            'next_day': '2024-12-02T20:00:00+03:00',
            'is_pleasant': True,
            'periodicity': 1,
            'time_to_complete': '02:00',
            'is_public': True
        }

        response_2 = self.client.post(url, data_2)

        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response_2.json(),
            {'id': 3,
             'time_to_complete': '02:00',
             'periodicity': 1,
             'related_habit': None,
             'place': 'Локально',
             'action': 'Приятная привычка',
             'start_day': '2024-12-02T20:00:00+03:00',
             'next_day': '2024-12-02T20:00:00+03:00',
             'is_pleasant': True,
             'reward': None,
             'is_public': True,
             'owner': 1}
        )

        self.assertEqual(Habit.objects.all().count(), 3)

        # Создание полезной привычки с привязкой к приятной привычке
        habit_3 = Habit.objects.get(id=3)
        data_3 = {
            'place': 'Локально',
            'action': 'Test',
            'start_day': '2024-12-02T20:00:00+03:00',
            'next_day': '2024-12-02T20:00:00+03:00',
            'related_habit': habit_3.id,
            'time_to_complete': '02:00'
        }

        response_3 = self.client.post(url, data_3)
        self.assertEqual(response_3.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response_3.json(),
            {'id': 4,
             'time_to_complete': '02:00',
             'periodicity': 1,
             'related_habit': 3,
             'place': 'Локально',
             'action': 'Test',
             'start_day': '2024-12-02T20:00:00+03:00',
             'next_day': '2024-12-02T20:00:00+03:00',
             'is_pleasant': False,
             'reward': None,
             'is_public': False,
             'owner': 1}
        )
        self.assertEqual(Habit.objects.all().count(), 4)

    def test_habit_retrieve(self):
        """Тестирование получение привычки."""
        url = reverse('habits:habits-detail', args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(data.get('place'), self.habit.place)
        self.assertEqual(data.get('action'), 'Test')
        self.assertEqual(data.get('start_day'), self.habit.start_day)

    def test_habit_update(self):
        """Тестирование обновления привычки"""
        url = reverse('habits:habits-update', args=(self.habit.pk,))
        data = {
            'place': 'Обновленное место'
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('place'), 'Обновленное место')

    def test_habit_delete(self):
        """Тестирование удаление привычки."""
        url = reverse('habits:habits-delete', args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_list(self):
        """Тестирование вывода списка привычек."""
        url = reverse('habits:habits-list')
        response = self.client.get(url)
        data = response.json()

        result = {"count": 1,
                  "next": None,
                  "previous": None,
                  "results": [
                      {
                          "id": self.habit.pk,
                          "time_to_complete": self.habit.time_to_complete,
                          "periodicity": self.habit.periodicity,
                          "place": self.habit.place,
                          "action": self.habit.action,
                          "start_day": self.habit.start_day,
                          "next_day": self.habit.next_day,
                          "is_pleasant": False,
                          "reward": self.habit.reward,
                          "is_public": False,
                          "owner": self.user.pk,
                          "related_habit": None
                      },
                  ]
                  }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
