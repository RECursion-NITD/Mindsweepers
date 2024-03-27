from django.urls import path, include
from .views import (
    MathsWordleView
)

urlpatterns = [
    path('test/', MathsWordleView.as_view(), name='game'),
]