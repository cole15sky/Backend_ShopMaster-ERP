from rest_framework import serializers

from .models import Order, OrderItem
from products.models import ProductVariant


class OrderItemCreateSerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class OrderCreateSerializer(serializers.ModelSerializer):

    items = OrderItemCreateSerializer(
        many=True,
        write_only=True
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "items",
        ]

    def create(self, validated_data):

        items_data = validated_data.pop("items")

        customer = self.context["request"].user

        order = Order.objects.create(
            customer=customer
        )

        total = 0

        for item in items_data:

            variant = ProductVariant.objects.get(
                id=item["variant_id"]
            )

            quantity = item["quantity"]

            price = variant.final_price

            OrderItem.objects.create(
                order=order,
                variant=variant,
                quantity=quantity,
                price=price
            )

            total += price * quantity

        order.total_amount = total
        order.save()

        return order

class OrderItemSerializer(serializers.ModelSerializer):

    product_name = serializers.CharField(
        source="variant.product.name",
        read_only=True
    )

    sku = serializers.CharField(
        source="variant.sku",
        read_only=True
    )

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product_name",
            "sku",
            "quantity",
            "price",
        ]
        
class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "status",
            "total_amount",
            "created_at",
            "items",
        ]