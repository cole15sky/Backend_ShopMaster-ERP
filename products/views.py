from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import (
    Brand,
    Category,
    Product,
    ProductVariant,
    ProductImage,
)


# -------------------------
# Brand Views
# -------------------------

class BrandListView(APIView):

    def get(self, request):
        brands = Brand.objects.all().values()
        return Response(brands)

    def post(self, request):
        name = request.data.get("name")

        brand = Brand.objects.create(
            name=name
        )

        return Response({"id": brand.id})


# -------------------------
# Category Views
# -------------------------

class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.all().values()
        return Response(categories)

    def post(self, request):
        name = request.data.get("name")
        parent_id = request.data.get("parent")

        parent = None

        if parent_id:
            parent = Category.objects.get(id=parent_id)

        category = Category.objects.create(
            name=name,
            parent=parent,
        )

        return Response({"id": category.id})


# -------------------------
# Product Views
# -------------------------

class ProductListView(APIView):

    def get(self, request):

        products = Product.objects.all().values(
            "id",
            "name",
            "brand__name",
            "category__name",
        )

        return Response(products)

    def post(self, request):

        name = request.data.get("name")
        brand_id = request.data.get("brand")
        category_id = request.data.get("category")

        brand = None
        category = None

        if brand_id:
            brand = Brand.objects.get(id=brand_id)

        if category_id:
            category = Category.objects.get(id=category_id)

        product = Product.objects.create(
            name=name,
            brand=brand,
            category=category,
        )

        return Response({"id": product.id})


# -------------------------
# Variant Views
# -------------------------

class VariantListView(APIView):

    def get(self, request):

        variants = ProductVariant.objects.all().values(
            "id",
            "sku",
            "price",
            "size",
            "color",
            "product__name",
        )

        return Response(variants)

    def post(self, request):

        product_id = request.data.get("product")
        size = request.data.get("size")
        color = request.data.get("color")
        sku = request.data.get("sku")
        price = request.data.get("price")

        product = Product.objects.get(id=product_id)

        variant = ProductVariant.objects.create(
            product=product,
            size=size,
            color=color,
            sku=sku,
            price=price,
        )

        return Response({"id": variant.id})


# -------------------------
# Product Detail View
# -------------------------

class ProductDetailView(APIView):

    def get(self, request, pk):

        product = Product.objects.get(id=pk)

        variants = product.variants.all().values()

        data = {
            "id": product.id,
            "name": product.name,
            "variants": list(variants),
        }

        return Response(data)