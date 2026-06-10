from rest_framework import serializers
from .models import Brand, Category, Product, ProductVariant, ProductImage
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
            "product",
            "id",
            "size",
            "gender",
            "color",
            "sku",
            "price",
            "discount_price",
            "cost_price",
            "barcode",
            "qr_code",
            "is_active",
        ]

        
class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "product",
            "image",
            "is_primary",   
        )

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(),source="brand",write_only=True,required=False,allow_null=True,)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source="category",write_only=True,required=False,allow_null=True,)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "brand",
            "brand_id",
            "category",
            "category_id",
            "description",
            "status",
            "slug",
            "created_at",
            "updated_at",
            "variants",
            "images",
        ]
        
class StockHistorySerializer(serializers.Serializer):
    variant_id = serializers.IntegerField()
    history = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField()),
        help_text="List of stock history records"
    )