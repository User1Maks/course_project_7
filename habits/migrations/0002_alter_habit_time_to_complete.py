# Generated by Django 5.1.3 on 2024-12-02 20:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="time_to_complete",
            field=models.CharField(
                blank=True,
                default=datetime.timedelta(seconds=120),
                help_text="Укажите время на выполнение привычки (не более 2 мин)",
                max_length=50,
                verbose_name="Время на выполнение привычки",
            ),
        ),
    ]
