from django.db import models


class UserRole(models.TextChoices):

    ADMIN = "ADMIN", "Admin"
    STAFF = "STAFF", "Staff"
    CUSTOMER = "CUSTOMER", "Customer"
    
class GenderType(models.TextChoices):
    MALE = "Male", "Male"
    FEMALE = "Female", "Female"
    UNISEX = "Unisex", "Unisex"

class SizeType(models.TextChoices):
    XS = "XS", "Extra Small"
    S = "S", "Small"
    M = "M", "Medium"
    L = "L", "Large"
    XL = "XL", "Extra Large"
    XXL = "XXL", "Double Extra Large"

class ProductStatus(models.TextChoices):
    ACTIVE = "Active", "Active"
    INACTIVE = "Inactive", "Inactive"