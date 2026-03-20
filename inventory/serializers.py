from rest_framework import serializers
from .models.inventory import Inventory


class InventorySerializer(serializers.ModelSerializer):

    variant_name = serializers.CharField(
        source="variant.__str__",
        read_only=True
    )

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True
    )

    class Meta:
        model = Inventory
        fields = [
            "id",
            "variant",
            "variant_name",
            "product_name",
            "quantity",
            "low_stock_alert",
            "updated_at",
        ]