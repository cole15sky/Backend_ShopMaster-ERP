from django.db import models
from .product import Product


class ProductVariant(models.Model):

    SIZE_CHOICES = [
        ("XS", "XS"),
        ("S", "S"),
        ("M", "M"),
        ("L", "L"),
        ("XL", "XL"),
        ("XXL", "XXL"),
    ]

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )

    size = models.CharField(
        max_length=10,
        choices=SIZE_CHOICES,
        null=True,
        blank=True,
    )

    color = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    sku = models.CharField(
        max_length=100,
        unique=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    barcode = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    qr_code = models.ImageField(
        upload_to="qr/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"