from rest_framework import serializers

from users.models import User
from .models import Organization


class TrialRegistrationSerializer(serializers.Serializer):

    business_name = serializers.CharField(max_length=255)
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True,min_length=8)
    password2 = serializers.CharField(write_only=True,min_length=8)

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists."
            )

        return value

    def validate(self, attrs):

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password": "Passwords do not match."
                }
            )

        return attrs


class OrganizationSerializer(serializers.ModelSerializer):

    owner_email = serializers.CharField(source="owner.email",read_only=True)
    trial_days_remaining = serializers.ReadOnlyField()
    trial_expired = serializers.ReadOnlyField()

    class Meta:
        model = Organization

        fields = [
            "id",
            "name",
            "owner_email",
            "is_trial",
            "trial_ends_at",
            "trial_days_remaining",
            "trial_expired",
            "is_active",
            "created_at",
        ]


class OrganizationMeSerializer(serializers.ModelSerializer):

    trial_days_remaining = serializers.ReadOnlyField()
    trial_expired = serializers.ReadOnlyField()

    class Meta:
        model = Organization

        fields = [
            "id",
            "name",
            "is_trial",
            "trial_ends_at",
            "trial_days_remaining",
            "trial_expired",
            "is_active",
        ]