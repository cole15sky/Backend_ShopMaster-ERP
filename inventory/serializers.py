from rest_framework import serializers
from products.models.product_variant import ProductVariant
from utils.enum import UnitType


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