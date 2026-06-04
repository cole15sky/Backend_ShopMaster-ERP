from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomerViewSet,
    CustomerAddressViewSet,
    CartViewSet,
    CartItemViewSet,
    ReviewViewSet,
    WishlistViewSet,
)

router = DefaultRouter()

router.register(
    
r"customers",CustomerViewSet,basename="customers")
router.register(r"customer-addresses",CustomerAddressViewSet,basename="customer-addresses")
router.register(r"carts",CartViewSet,basename="carts")
router.register(r"cart-items",CartItemViewSet,basename="cart-items")
router.register(r"reviews",ReviewViewSet,basename="reviews")
router.register(r"wishlists",WishlistViewSet,basename="wishlists")

urlpatterns = [
    path("", include(router.urls)),
]