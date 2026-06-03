from django.urls import path

from .views import (
    StockInView,
    StockOutView,
    StockAdjustmentView,
    LowStockView,
)

urlpatterns = [
    path("", InventoryListView.as_view(), name="inventory-list"),
    path("stock-in/",StockInView.as_view(),name="stock-in",),
    path("stock-out/",StockOutView.as_view(),name="stock-out",),
    path("adjust/",StockAdjustmentView.as_view(),name="stock-adjust",),
    path("low-stock/",LowStockView.as_view(),name="low-stock",),
]