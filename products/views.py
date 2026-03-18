from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Brand, Category, Product, ProductVariant
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, ProductVariantSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=["get"])
    def variants(self, request, pk=None):
        product = self.get_object()
        serializer = ProductVariantSerializer(product.variants.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductVariantViewSet(viewsets.ModelViewSet):
    
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    

class StockHistoryViewSet(viewsets.ViewSet):
    @extend_schema(
        request=None,
        responses={200: "Stock history retrieved successfully"},
        description="Retrieve stock history for a product variant"
    )
    @action(detail=False, methods=["get"], url_path="variant/(?P<variant_id>[^/.]+)/history")
    def variant_history(self, request, variant_id=None):
        # Placeholder implementation
        return Response({"message": f"Stock history for variant {variant_id} retrieved successfully"}, status=status.HTTP_200_OK)