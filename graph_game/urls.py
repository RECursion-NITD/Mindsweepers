from django.urls import path, include
from .views import (
    GraphGameView,
    GraphGenerateView
)

urlpatterns = [
    path('validate/', GraphGameView.as_view(), name='create_game1'),
    path('generate/', GraphGenerateView.as_view(), name='create_game2'),
]