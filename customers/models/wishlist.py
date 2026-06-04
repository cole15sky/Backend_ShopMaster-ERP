from django.db import models
from .customer import Customer


class Wishlist(models.Model):

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.CASCADE,
        related_name="wishlist_entries"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "customer",
            "variant"
        )

    def __str__(self):
        return f"{self.customer.full_name} - {self.variant}"