from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BrandViewSet, CategoryViewSet, ProductViewSet, ProductVariantViewSet, StockHistoryViewSet

router = DefaultRouter()
router.register("brands", BrandViewSet, basename="brand")
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")
router.register("variants", ProductVariantViewSet, basename="variant")
router.register("stock_history", StockHistoryViewSet, basename="stock_history")

urlpatterns = [
    path("", include(router.urls)),
]