from rest_framework import serializers
from products.models.product_variant import ProductVariant
from utils.enum import UnitType
from .models.inventory import Inventory


class InventorySerializer(serializers.ModelSerializer):
    variant_name= serializers.CharField(source="variant.sku", read_only=True)
    is_low_stock = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = ["id", "variant", "variant_name", "quantity", "is_low_stock","low_stock_alert", "updated_at"]


class StockInSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    unit = serializers.ChoiceField(choices=UnitType.choices)
    note = serializers.CharField(required=False, allow_blank=True)


class StockOutSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    unit = serializers.ChoiceField(choices=UnitType.choices)
    note = serializers.CharField(required=False, allow_blank=True)


class StockAdjustmentSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    new_quantity = serializers.IntegerField(min_value=0)
    unit = serializers.ChoiceField(choices=UnitType.choices)
    note = serializers.CharField(required=False, allow_blank=True)


class LowStockItemSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    variant = serializers.CharField()
    stock = serializers.IntegerField()
    low_stock_alert = serializers.IntegerField()


class StockResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = serializers.DictField()