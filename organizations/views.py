from datetime import timedelta

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from users.models import User
from utils.enum import UserRole

from .models import Organization
from .serializers import TrialRegistrationSerializer


class TrialRegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = TrialRegistrationSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if User.objects.filter(
            email=data["email"]
        ).exists():
            return Response(
                {"message": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        organization = Organization.objects.create(
            name=data["business_name"],
            trial_ends_at=timezone.now() + timedelta(days=14)
        )

        user = User.objects.create_user(
            email=data["email"],
            full_name=data["full_name"],
            phone=data["phone"],
            role=UserRole.ADMIN,
            organization=organization,
            password=data["password"],
        )

        organization.owner = user
        organization.save()

        return Response(
            {
                "message": "Trial started successfully"
            },
            status=status.HTTP_201_CREATED
        )