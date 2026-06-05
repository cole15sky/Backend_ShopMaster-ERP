from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegistrationView, MeView, RoleBasedTokenObtainPairView, CustomerViewSet

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")
router.register(r"customers", CustomerViewSet, basename="customer")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
    path("login/", RoleBasedTokenObtainPairView.as_view(), name="role-login"),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    CustomerViewSet,
    UserRegistrationView,
    MeView,
    RoleBasedTokenObtainPairView,
    CustomerRegistrationView,
)

router = DefaultRouter()

router.register(r"staff",UserViewSet,basename="staff")
router.register(r"customers",CustomerViewSet,basename="customers")

urlpatterns = [
    path("login/", RoleBasedTokenObtainPairView.as_view(), name="login"),
    path("register/", UserRegistrationView.as_view(), name="staff-register"),
    path("customers/register/", CustomerRegistrationView.as_view(), name="customer-register"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
]