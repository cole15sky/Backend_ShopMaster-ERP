from django.db.models import F
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from products.models.product_variant import ProductVariant
from utils.enum import StockChangeType

from .models.inventory import Inventory
from .models.stock_history import StockHistory

from .serializers import (
    StockInSerializer,
    StockOutSerializer,
    StockAdjustmentSerializer,
    InventorySerializer,
    LowStockItemSerializer,
)


@extend_schema(
    responses=InventorySerializer(many=True),
    description="List inventory records"
)
class InventoryListView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Inventory.objects.select_related("variant")
    serializer_class = InventorySerializer


@extend_schema(
    request=StockInSerializer,
    responses={200: dict},
    description="Add stock to inventory"
)
class StockInView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = StockInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        variant = ProductVariant.objects.get(
            id=serializer.validated_data["variant_id"]
        )

        inventory, _ = Inventory.objects.get_or_create(
            variant=variant
        )

        previous_stock = inventory.quantity
        quantity = serializer.validated_data["quantity"]

        inventory.quantity += quantity
        inventory.save()

        StockHistory.objects.create(
            variant=variant,
            change_type=StockChangeType.STOCK_IN,
            quantity=quantity,
            unit=serializer.validated_data["unit"],
            previous_stock=previous_stock,
            new_stock=inventory.quantity,
            note=serializer.validated_data.get("note"),
            changed_by=request.user,
        )

        return Response(
            {
                "message": "Stock added successfully",
                "data": {
                    "previous_stock": previous_stock,
                    "new_stock": inventory.quantity,
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    request=StockOutSerializer,
    responses={200: dict},
    description="Deduct stock from inventory"
)
class StockOutView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = StockOutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        variant = ProductVariant.objects.get(
            id=serializer.validated_data["variant_id"]
        )

        inventory = Inventory.objects.get(
            variant=variant
        )

        quantity = serializer.validated_data["quantity"]

        if inventory.quantity < quantity:
            return Response(
                {
                    "message": "Insufficient stock."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        previous_stock = inventory.quantity

        inventory.quantity -= quantity
        inventory.save()

        StockHistory.objects.create(
            variant=variant,
            change_type=StockChangeType.STOCK_OUT,
            quantity=quantity,
            unit=serializer.validated_data["unit"],
            previous_stock=previous_stock,
            new_stock=inventory.quantity,
            note=serializer.validated_data.get("note"),
            changed_by=request.user,
        )

        return Response(
            {
                "message": "Stock deducted successfully",
                "data": {
                    "previous_stock": previous_stock,
                    "new_stock": inventory.quantity,
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    request=StockAdjustmentSerializer,
    responses={200: dict},
    description="Adjust inventory stock"
)
class StockAdjustmentView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = StockAdjustmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        variant = get_object_or_404(
            ProductVariant,
            id=serializer.validated_data["variant_id"]
        )

        inventory = Inventory.objects.select_for_update().get(
            variant=variant
        )

        previous_stock = inventory.quantity

        inventory.quantity = serializer.validated_data[
            "new_quantity"
        ]
        inventory.save()

        StockHistory.objects.create(
            variant=variant,
            change_type=StockChangeType.ADJUSTMENT,
            quantity=abs(
                previous_stock - inventory.quantity
            ),
            unit=serializer.validated_data["unit"],
            previous_stock=previous_stock,
            new_stock=inventory.quantity,
            note=serializer.validated_data.get("note"),
            changed_by=request.user,
        )

        return Response(
            {
                "message": "Stock adjusted successfully",
                "data": {
                    "previous_stock": previous_stock,
                    "new_stock": inventory.quantity,
                },
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    responses=LowStockItemSerializer(many=True),
    description="Retrieve products with low stock"
)
class LowStockView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Inventory.objects.filter(
            quantity__lte=F("low_stock_alert")
        )

        data = [
            {
                "variant_id": item.variant.id,
                "variant": str(item.variant),
                "stock": item.quantity,
                "low_stock_alert": item.low_stock_alert,
            }
            for item in queryset
        ]

        return Response(
            {
                "message": "Low stock products fetched successfully.",
                "data": data,
            }
        )