from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.enum import UserRole


class User(AbstractUser):

    username = None

    email = models.EmailField(
        unique=True,
    )

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.ADMIN,
    )

    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    profile_pic = models.ImageField(
        upload_to="users/profile/",
        blank=True,
        null=True,
    )

    position = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email