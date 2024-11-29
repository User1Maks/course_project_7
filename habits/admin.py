from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'place', 'time_habit', 'action',
                    'is_pleasant', 'reward', 'is_public', 'start_day',)
    search_fields = ('owner',)
    list_filter = ('id', 'owner', 'time_habit', 'is_pleasant', 'is_public',)
