from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from habits.models import NULLABLE


class User(AbstractUser):
    """Модель пользователя"""

    username = models.CharField(
        max_length=50,
        verbose_name='Никнейм пользователя',
        unique=True,
        help_text='Введите имя пользователя'
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        **NULLABLE,
        help_text='Введите адрес электронной почты'
    )
    phone = PhoneNumberField(
        verbose_name='Номер телефона',
        **NULLABLE,
        help_text='Введите Ваш номер телефона'
    )
    date_of_birth = models.DateField(
        verbose_name='Дата рождения',
        **NULLABLE,
        help_text='Введите дату Вашего рождения'
    )

    tg_chat_id = models.CharField(
        max_length=50,
        **NULLABLE,
        verbose_name='Телеграмм chat-id',
        help_text='Укажите телеграмм chat-id'
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
