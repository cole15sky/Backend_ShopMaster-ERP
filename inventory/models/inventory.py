from django.db import models
from products.models.product_variant import ProductVariant


class Inventory(models.Model):

    variant = models.OneToOneField(ProductVariant,on_delete=models.CASCADE,related_name="inventory")
    quantity = models.IntegerField(default=0)
    low_stock_alert = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.variant} - {self.quantity}"