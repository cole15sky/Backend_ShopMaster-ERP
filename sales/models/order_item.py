from django.db import models


class OrderItem(models.Model):

    order = models.ForeignKey(
        "sales.Order",
        related_name="items",
        on_delete=models.CASCADE
    )


    variant = models.ForeignKey(
        "products.ProductVariant",
        on_delete=models.PROTECT
    )


    quantity = models.PositiveIntegerField(
        default=1
    )


    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )