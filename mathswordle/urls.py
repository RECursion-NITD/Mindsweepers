from django.urls import path, include
from .views import (
    CreateMathsWordleView,
    ValidateStringView,
    CreateGameState
)

urlpatterns = [
    path('create/', CreateMathsWordleView.as_view(), name='create_game1'),
    path('validate/', ValidateStringView.as_view(), name='validate'),
    path('gamestring/', CreateGameState.as_view(), name='gamestring')
]