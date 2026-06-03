from django.db import models
from products.models.product_variant import ProductVariant


class Inventory(models.Model):

    variant = models.OneToOneField( ProductVariant,on_delete=models.CASCADE,related_name="inventory")
    quantity = models.PositiveIntegerField(default=0)
    low_stock_alert = models.PositiveIntegerField(default=10)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_alert

    def __str__(self):
        return f"{self.variant} - {self.quantity}"