from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from quizhub.models.question_models import Question, FavoriteQuestion, ReadQuestion
from django.shortcuts import get_object_or_404

User = get_user_model()

# Registration View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=RegisterSerializer,
        operation_description="Register a new user with email and password",
        responses={201: 'User registered successfully', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Custom login view using Simple JWT's TokenObtainPairView
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class FavoriteQuestionUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        favorite, created = FavoriteQuestion.objects.get_or_create(user=request.user, question=question)

        if favorite.is_favorite:
            favorite.is_favorite = False
            message = 'Question removed from favorites.'
        else:
            favorite.is_favorite = True
            message = 'Question marked as favorite.'

        favorite.save()
        return Response({'message': message}, status=status.HTTP_200_OK)
    

class ReadQuestionUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        read_status, created = ReadQuestion.objects.get_or_create(user=request.user, question=question)

        if read_status.is_read:
            read_status.is_read = False
            message = 'Question marked as unread.'
        else:
            read_status.is_read = True
            message = 'Question marked as read.'

        read_status.save()
        return Response({'message': message}, status=status.HTTP_200_OK)