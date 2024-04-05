from django.urls import path, include
from .views import (
    LoginView,
    RegisterView,
    FetchRankings
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('ranking/', FetchRankings.as_view(), name='ranking'),
]