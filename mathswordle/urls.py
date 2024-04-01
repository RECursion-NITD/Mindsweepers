from django.urls import path, include
from .views import (
    CreateMathsWordleView,
    ValidateStringView,
)

urlpatterns = [
    path('create/', CreateMathsWordleView.as_view(), name='create_game1'),
    path('validate/', ValidateStringView.as_view(), name='validate'),
]