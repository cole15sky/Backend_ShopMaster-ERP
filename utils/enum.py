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
    
class StockChangeType(models.TextChoices):
    """
    Used in StockHistory model
    """

    ADD = "ADD", "Add Stock"
    REMOVE = "REMOVE", "Remove Stock"
    SALE = "SALE", "Sale"
    RETURN = "RETURN", "Return"
    ADJUST = "ADJUST", "Manual Adjust"
    
class UnitType(models.TextChoices):
    PIECE = "PCS", "Piece"
    KG = "KG", "Kilogram"
    GRAM = "G", "Gram"
    LITER = "L", "Liter"
    BOX = "BOX", "Box"
    PACK = "PACK", "Pack"

class SubscriptionStatus(models.TextChoices):
    TRIAL = "TRIAL", "Trial"
    ACTIVE = "ACTIVE", "Active"
    EXPIRED = "EXPIRED", "Expired"
    CANCELLED = "CANCELLED", "Cancelled"