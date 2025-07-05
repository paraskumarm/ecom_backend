from django.db import models

from api.address.models import Address
from api.product.models import Product
from api.user.models import CustomUser


class OrderPayTm(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    products = models.ManyToManyField(Product)
    transaction_id = models.IntegerField()
    product_names = models.CharField(max_length=500)
    total_products = models.CharField(max_length=500, default=0)
    total_amount = models.CharField(max_length=50, default=0)
    isPaid = models.BooleanField(default=False)
    order_payment_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.transaction_id)
