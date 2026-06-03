from rest_framework import serializers

from .models.customer import Customer
from .models.address import CustomerAddress
from .models.cart import Cart
from .models.cart_item import CartItem
from .models.review import Review
from .models.wishlist import Wishlist


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = (
            "id",
            "full_name",
            "email",
            "phone",
            "profile_picture",
            "date_of_birth",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class CustomerAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerAddress
        fields = (
            "id",
            "customer",
            "address_type",
            "full_name",
            "phone",
            "province",
            "district",
            "city",
            "ward",
            "address_line",
            "landmark",
            "is_default",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = (
            "id",
            "customer",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = (
            "id",
            "cart",
            "variant",
            "quantity",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = (
            "id",
            "customer",
            "product",
            "rating",
            "comment",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = (
            "id",
            "customer",
            "variant",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
        )