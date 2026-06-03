from django.db import models
from .customer import Customer
from .utils.enum import CustomerAddressType


class CustomerAddress(models.Model):


    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="addresses"
    )

    address_type = models.CharField(
        max_length=20,
        choices=CustomerAddressType.choices,
        default=CustomerAddressType.HOME
    )

    full_name = models.CharField(
        max_length=255
    )

    phone = models.CharField(
        max_length=20
    )


    province = models.CharField(
        max_length=100
    )

    district = models.CharField(
        max_length=100
    )

    city = models.CharField(
        max_length=100
    )

    ward = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )


    address_line = models.TextField()

    landmark = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_default = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.customer.full_name} - {self.address_type}"