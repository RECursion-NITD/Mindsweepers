from django.urls import path, include
from .views import (
    GraphGameView,
    CreateGraphGameView,
    GetGraphView
)

urlpatterns = [
    path('validate/', GraphGameView.as_view(), name='create_game1'),
    path('generate/', CreateGraphGameView.as_view(), name='create_game2'),
    path('fetch/', GetGraphView.as_view(), name='fetch_game3'),
]