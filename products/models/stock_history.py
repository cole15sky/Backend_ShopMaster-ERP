from django.db import models
from .product_variant import ProductVariant
from users.models import User
from utils.enum import StockChangeType, UnitType


class StockHistory(models.Model):

    variant = models.ForeignKey(ProductVariant,on_delete=models.CASCADE,related_name="stock_history",)
    change_type = models.CharField(max_length=10,choices=StockChangeType.choices,)
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10,choices=UnitType.choices,)
    previous_stock = models.IntegerField()
    new_stock = models.IntegerField()
    note = models.TextField(blank=True,null=True,)
    changed_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,)
    created_at = models.DateTimeField(auto_now_add=True,)