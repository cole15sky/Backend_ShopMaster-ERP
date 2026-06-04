from django.db import models


class CartItem(models.Model):

    cart = models.ForeignKey(
        "customers.Cart",
        on_delete=models.CASCADE,
        related_name="items"
    )

    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "cart",
            "variant"
        )

    def __str__(self):
        return f"{self.variant} x {self.quantity}"