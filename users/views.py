from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from .serializers import UserRegistrationSerializer, UserSerializer, MeSerializer
from .models import User

# Custom Response
class CustomResponse:
    @staticmethod
    def success(message, data=None, status_code=status.HTTP_200_OK):
        return Response({"message": message, "data": data}, status=status_code)

    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({"message": message}, status=status_code)


class UserRegistrationView(APIView):
    """
    Endpoint for registering new users (admin only can create other users).
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return CustomResponse.success(
                message="User created successfully",
                data=UserSerializer(user).data,
                status_code=status.HTTP_201_CREATED
            )


class UserViewSet(GenericViewSet):
    """
    ViewSet for listing, soft deleting, and managing users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        role_filter = request.query_params.get("role")
        queryset = User.objects.filter(is_active=True)
        if role_filter:
            queryset = queryset.filter(role=role_filter)
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success("Fetched users successfully.", serializer.data)

    @action(detail=True, methods=["delete"], url_path="soft-delete")
    def soft_delete(self, request, pk=None):
        user = self.get_object()
        if not user.is_active:
            return CustomResponse.error("User already inactive.", status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return CustomResponse.success("User soft deleted successfully.")

    @action(detail=False, methods=["get"], url_path="soft-deleted")
    def list_soft_deleted(self, request):
        queryset = User.objects.filter(is_active=False)
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success("Fetched soft deleted users.", serializer.data)

    @action(detail=True, methods=["patch"], url_path="recover")
    def recover_user(self, request, pk=None):
        user = self.get_object()
        if user.is_active:
            return CustomResponse.error("User is already active.", status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        return CustomResponse.success("User recovered successfully.")


class MeView(APIView):
    """
    Endpoint to get current authenticated user info.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return CustomResponse.success("Fetched current user.", serializer.data)