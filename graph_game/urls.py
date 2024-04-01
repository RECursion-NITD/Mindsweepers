from django.urls import path, include
from .views import (
    GraphGameView,
)

urlpatterns = [
    path('test/', GraphGameView.as_view(), name='create_game1'),
]