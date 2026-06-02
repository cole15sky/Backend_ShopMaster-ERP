from django.db import models
from products.models.product_variant import ProductVariant
from users.models import User
from utils.enum import StockChangeType, UnitType


class StockHistory(models.Model):

    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="stock_history",
    )

    change_type = models.CharField(
        max_length=20,
        choices=StockChangeType.choices,
    )

    quantity = models.PositiveIntegerField()

    unit = models.CharField(
        max_length=10,
        choices=UnitType.choices,
    )

    previous_stock = models.PositiveIntegerField()

    new_stock = models.PositiveIntegerField()

    note = models.TextField(
        blank=True,
        null=True,
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["variant"]),
            models.Index(fields=["created_at"]),
        ]