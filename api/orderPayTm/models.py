
from django.db import models
from api.address.models import Address
from api.user.models import CustomUser
from api.product.models import Product

# Create your models here.


class OrderPayTm(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product)
    product_names = models.CharField(max_length=500)
    total_products = models.CharField(max_length=500, default=0)
    total_amount = models.CharField(max_length=50, default=0)
    quantity_info = models.CharField(max_length=500,default="",null=True)
    color_info = models.CharField(max_length=500,default="",null=True)
    size_info = models.CharField(max_length=500,default="",null=True)
    status_info = models.CharField(max_length=500,default="",null=True)
    isPaid=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
            return self.user.name
