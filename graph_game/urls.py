from django.urls import path, include
from .views import (
    GraphGameView,
)

urlpatterns = [
    path('generate_tree/', GraphGameView.as_view(), name='generate_tree'),
    path('validate_tree/', GraphGameView.as_view(), name='validate_tree'),
]