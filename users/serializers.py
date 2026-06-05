from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from utils.enum import UserRole


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user info (admin view).
    """
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "phone", "position", "profile_pic", "is_active"]
    
    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")

        return Usser.objects.create_user(**validated_data, password=password)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["email", "full_name", "phone", "position", "password", "password2"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MeSerializer(serializers.ModelSerializer):
    """
    Serializer for currently authenticated user.
    """
    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role", "phone", "position", "profile_pic"]
        

class RoleBasedTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT serializer that validates role on login.
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        requested_role = self.context['request'].data.get("role")
        if requested_role and user.role != requested_role:
            raise serializers.ValidationError("Unauthorized role login.")

        # Add user info in response
        data.update({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
        })
        return data


class CustomerRegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "full_name",
            "phone",
            "password",
            "password2",
            "profile_pic"
        )

    def validate(self, attrs):

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):

        validated_data.pop("password2")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            role=UserRole.CUSTOMER,
            password=password,
            **validated_data
        )

        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
            "Email already exists."
        )
        return value
        

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "profile_pic",
            "is_active",
            "date_joined",
        )

class CustomerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "full_name",
            "phone",
            "profile_pic",
        ) 


