from django.db import models


class UserRole(models.TextChoices):

    ADMIN = "ADMIN", "Admin"
    STAFF = "STAFF", "Staff"
    CUSTOMER = "CUSTOMER", "Customer"