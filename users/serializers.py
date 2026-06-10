from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User

from .models import User
from utils.enum import UserRole


# USER SERIALIZERS (STAFF/ADMIN)

class UserSerializer(serializers.ModelSerializer):
    """
    Base serializer for admin/user listing.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "phone",
            "position",
            "profile_pic",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined", "role"]
    

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Admin creates staff users.
    """
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "phone",
            "position",
            "password",
            "password2",
        ]
        fields = [
            "email",
            "full_name",
            "phone",
            "position",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            **validated_data,
            password=password,
            role=UserRole.STAFF
        )
        return user
    

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    """
    Public customer signup serializer.
    """

    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "phone",
            "password",
            "password2",
            "profile_pic",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            **validated_data,
            password=password,
            role=UserRole.CUSTOMER
        )
        return user

class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer registration serializer.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "phone",
            "profile_pic",
            "is_active",
            "date_joined",
        ]
        read_only_fields = ["id", "date_joined"]


class CustomerUpdateSerializer(serializers.ModelSerializer):
    """
    Customer profile update.
    """

    class Meta:
        model = User
        fields = [
            "full_name",
            "phone",
            "profile_pic",
        ]

class RoleBasedTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT login with role validation.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        requested_role = self.context["request"].data.get("role")

        if requested_role and user.role != requested_role:
            raise serializers.ValidationError("Unauthorized role login.")

        data.update({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
        })
        return data

class MeSerializer(serializers.ModelSerializer):
    """
    Current logged-in user.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "phone",
            "position",
            "profile_pic",
        ]