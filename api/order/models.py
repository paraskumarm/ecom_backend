from django.db import models
from api.user.models import CustomUser
from api.product.models import Product
from api.address.models import Address

class Order(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    transaction_id = models.IntegerField(default=0)
    product_name = models.CharField(max_length=500)
    total_products = models.CharField(max_length=500, default=0)
    total_amount = models.CharField(max_length=50, default=0)
    quantity_info = models.CharField(max_length=100, default="", null=True)
    color_info = models.CharField(max_length=100, default="", null=True)
    size_info = models.CharField(max_length=100, default="", null=True)
    status_info = models.CharField(max_length=100, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.transaction_id)
