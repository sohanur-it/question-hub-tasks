from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, FavoriteQuestionUpdateView, ReadQuestionUpdateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),  # Login URL
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh
    path('questions/<int:question_id>/favorite/', FavoriteQuestionUpdateView.as_view(), name='update-favorite'),
    path('questions/<int:question_id>/read/', ReadQuestionUpdateView.as_view(), name='update-read'),
]