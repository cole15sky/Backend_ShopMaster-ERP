from django.urls import path
from .views import UserRegistrationView, UserViewSet, MeView

user_list = UserViewSet.as_view({"get": "list"})
soft_deleted = UserViewSet.as_view({"get": "list_soft_deleted"})

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("me/", MeView.as_view(), name="me"),
    path("users/", user_list, name="user-list"),
    path("users/soft-deleted/", soft_deleted, name="user-soft-deleted"),
]