from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import BasePermission

from utils.enum import UserRole
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, CustomerRegistrationSerializer, CustomerUpdateSerializer, RoleBasedTokenObtainPairSerializer, MeSerializer
from customers.serializers import CustomerSerializer


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "ADMIN"
        )
        
# RESPONSE WRAPPER
class CustomResponse:

    @staticmethod
    def success(message, data=None, status_code=status.HTTP_200_OK):
        return Response(
            {"message": message, "data": data},
            status=status_code
        )

    @staticmethod
    def error(message, status_code=status.HTTP_400_BAD_REQUEST):
        return Response(
            {"message": message},
            status=status_code
        )


# USER REGISTER (STAFF / ADMIN)

class UserRegistrationView(APIView):
    permission_classes = [IsAdminRole]
    serializer_class = UserRegistrationSerializer

    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return CustomResponse.success(
            "User created successfully.",
            UserSerializer(user).data,
            status.HTTP_201_CREATED
        )


# CUSTOMER REGISTER (PUBLIC)

class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomerRegistrationSerializer

    def post(self, request):

        serializer = CustomerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = serializer.save()

        return CustomResponse.success(
            "Customer registered successfully.",
            CustomerRegistrationSerializer(customer).data,
            status.HTTP_201_CREATED
        )


# USER MANAGEMENT (STAFF ONLY)

class UserViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.exclude(role=UserRole.CUSTOMER)

    serializer_class = UserSerializer

    @action(detail=True, methods=["delete"])
    def soft_delete(self, request, pk=None):

        user = self.get_object()

        if not user.is_active:
            return CustomResponse.error("User already inactive.")

        user.is_active = False
        user.save()

        return CustomResponse.success("User soft deleted.")


    @action(detail=True, methods=["patch"])
    def recover(self, request, pk=None):

        user = self.get_object()

        if user.is_active:
            return CustomResponse.error("User already active.")

        user.is_active = True
        user.save()

        return CustomResponse.success("User recovered.")


    @action(detail=False, methods=["get"])
    def soft_deleted(self, request):

        users = User.objects.filter(is_active=False).exclude(role=UserRole.CUSTOMER)

        return CustomResponse.success(
            "Soft deleted users",
            UserSerializer(users, many=True).data
        )


# CUSTOMER MANAGEMENT

class CustomerViewSet(ModelViewSet):

    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.filter(role=UserRole.CUSTOMER)

    def get_serializer_class(self):

        if self.action in ["update", "partial_update"]:
            return CustomerUpdateSerializer

        return CustomerRegistrationSerializer

    @action(detail=True, methods=["delete"])
    def soft_delete(self, request, pk=None):

        customer = self.get_object()

        if not customer.is_active:
            return CustomResponse.error("Customer already inactive.")

        customer.is_active = False
        customer.save()

        return CustomResponse.success("Customer soft deleted.")


    @action(detail=True, methods=["patch"])
    def recover(self, request, pk=None):

        customer = self.get_object()

        if customer.is_active:
            return CustomResponse.error("Customer already active.")

        customer.is_active = True
        customer.save()

        return CustomResponse.success("Customer recovered.")


    @action(detail=False, methods=["get"])
    def soft_deleted(self, request):

        customers = User.objects.filter(
            role=UserRole.CUSTOMER,
            is_active=False
        )

        return CustomResponse.success(
            "Soft deleted customers",
            CustomerSerializer(customers, many=True).data
        )


# ME

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeSerializer

    def get(self, request):
        return CustomResponse.success(
            "Current user",
            MeSerializer(request.user).data
        )


# LOGIN

class RoleBasedTokenObtainPairView(TokenObtainPairView):
    serializer_class = RoleBasedTokenObtainPairSerializer