from django.db import models
from .product_variant import ProductVariant

class StockHistory(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="stock_history")
    previous_stock = models.PositiveIntegerField()
    added_stock = models.PositiveIntegerField()
    current_stock = models.PositiveIntegerField()
    reason = models.CharField(max_length=255, blank=True, null=True)  # purchase, sale, adjustment
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.variant.sku} - {self.current_stock}"