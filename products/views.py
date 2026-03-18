from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models.stock_history import StockHistory
from .models.product_variant import ProductVariant
from .models import Brand, Category, Product, ProductVariant, StockHistory
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer, ProductVariantSerializer, StockHistorySerializer

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
    queryset = ProductVariant.objects.none()  # Needed for swagger

    @extend_schema(
        request=None,
        responses={200: StockHistorySerializer},
        description="Retrieve stock history for a product variant"
    )
    @action(
        detail=False,
        methods=["get"],
        url_path=r"variant/(?P<variant_id>\d+)/history"
    )
    def variant_history(self, request, variant_id=None):
        try:
            variant_id = int(variant_id)
        except ValueError:
            return Response({"error": "Invalid variant_id"}, status=400)

        history_qs = StockHistory.objects.filter(variant_id=variant_id)

        stock_history = [
            {
                "type": h.change_type,
                "quantity": str(h.quantity),
                "unit": h.unit,
                "date": h.created_at.strftime("%Y-%m-%d"),
                "note": h.note or ""
            }
            for h in history_qs
        ]

        data = {
            "variant_id": variant_id,
            "history": stock_history
        }

        serializer = StockHistorySerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)