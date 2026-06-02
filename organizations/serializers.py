from rest_framework import serializers


class TrialRegistrationSerializer(serializers.Serializer):
    business_name = serializers.CharField(max_length=255)
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match"}
            )
        return attrs