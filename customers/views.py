from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models.customer import Customer
from .models.address import CustomerAddress
from .models.cart import Cart
from .models.cart_item import CartItem
from .models.review import Review
from .models.wishlist import Wishlist

from .serializers import (
    CustomerSerializer,
    CustomerAddressSerializer,
    CartSerializer,
    CartItemSerializer,
    ReviewSerializer,
    WishlistSerializer,
)


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        "full_name",
        "email",
        "phone",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "full_name",
    ]


class CustomerAddressViewSet(ModelViewSet):
    queryset = CustomerAddress.objects.select_related(
        "customer"
    )
    serializer_class = CustomerAddressSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.select_related(
        "customer"
    )
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.select_related(
        "cart",
        "variant",
    )
    serializer_class = CartItemSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related(
        "customer",
        "product",
    )
    serializer_class = ReviewSerializer


class WishlistViewSet(ModelViewSet):
    queryset = Wishlist.objects.select_related(
        "customer",
        "variant",
    )
    serializer_class = WishlistSerializer