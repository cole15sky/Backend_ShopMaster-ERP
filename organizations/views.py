from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from users.models import User
from utils.enum import UserRole
from .models import Organization
from .serializers import TrialRegistrationSerializer

@extend_schema(tags=["Organizations"],request=TrialRegistrationSerializer)

class TrialRegistrationView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TrialRegistrationSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        organization = Organization.objects.create(
            name=data["business_name"],
            is_trial=True,
            is_active=True,
            trial_ends_at=timezone.now() + timedelta(days=14),
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
        organization.save(update_fields=["owner"])

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Trial started successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
            },
            "organization": {
                "id": organization.id,
                "name": organization.name,
                "is_trial": organization.is_trial,
                "trial_days_remaining": organization.trial_days_remaining,
                "trial_expired": organization.trial_expired,
            },
        }, status=status.HTTP_201_CREATED)