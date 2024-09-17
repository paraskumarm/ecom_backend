from django.db import models
from api.address.models import Address
from api.user.models import CustomUser
from api.product.models import Product


class OrderCOD(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    products = models.ManyToManyField(Product)
    # products = models.ForeignKey(
    # Product, on_delete=models.CASCADE, null=True, blank=True)
    product_names = models.CharField(max_length=500)
    transaction_id = models.IntegerField()
    total_products = models.CharField(max_length=500, default=0)
    total_amount = models.CharField(max_length=50, default=0)
    isPaid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.transaction_id)
