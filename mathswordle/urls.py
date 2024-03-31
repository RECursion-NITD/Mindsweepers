from django.urls import path, include
from .views import (
    MathsWordleView,
    ValidateStringView,
)

urlpatterns = [
    
    path('test/', MathsWordleView.as_view(), name='game'),
    path('validate/', ValidateStringView.as_view(), name='validate'),
]