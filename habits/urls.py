from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (
    HabitCreateAPIView,
    HabitDestroyAPIView,
    HabitListAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    # Habit
    path("create/", HabitCreateAPIView.as_view(), name="habits-create"),
    path("list/", HabitListAPIView.as_view(), name="habits-list"),
    path("detail/<int:pk>/", HabitRetrieveAPIView.as_view(),
         name="habits-detail"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(),
         name="habits-update"),
    path("delete/<int:pk>/", HabitDestroyAPIView.as_view(),
         name="habits-delete"),
]
