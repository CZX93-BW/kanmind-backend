from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    EmailCheckSerializer,
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
)


User = get_user_model()


class RegistrationView(GenericAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.create(user=user)
        response_data = {
            "token": token.key,
            "fullname": user.fullname,
            "email": user.email,
            "user_id": user.pk,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        response_data = {
            "token": token.key,
            "fullname": user.fullname,
            "email": user.email,
            "user_id": user.pk,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class EmailCheckView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EmailCheckSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            self.get_queryset(),
            email=serializer.validated_data["email"],
        )
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)