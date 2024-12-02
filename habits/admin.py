from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'place', 'action', 'is_pleasant', 'reward',
                    'is_public', 'start_day',)
    search_fields = ('owner',)
    list_filter = ('id', 'owner', 'is_pleasant', 'is_public',)
