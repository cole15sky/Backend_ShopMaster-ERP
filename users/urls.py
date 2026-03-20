from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegistrationView, MeView, RoleBasedTokenObtainPairView

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("me/", MeView.as_view(), name="me"),
    path("", include(router.urls)),
    path("login/", RoleBasedTokenObtainPairView.as_view(), name="role-login"),
]