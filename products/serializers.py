from rest_framework import serializers
from .models import Brand, Category, Product, ProductVariant
from utils.enum import SizeType, GenderType, ProductStatus

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "logo", "is_active"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent", "is_active"]

class ProductVariantSerializer(serializers.ModelSerializer):
    size = serializers.ChoiceField(choices=SizeType.choices)
    gender = serializers.ChoiceField(choices=GenderType.choices)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "size",
            "gender",
            "color",
            "sku",
            "price",
            "discount_price",
            "cost_price",
            "stock_quantity",
            "barcode",
            "qr_code",
            "is_active",
        ]

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "category",
            "description",
            "status",
            "slug",
            "created_at",
            "updated_at",
            "variants",
        ]