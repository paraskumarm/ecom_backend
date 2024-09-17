from django.db import models

from api.product.models import Product

# Create your models here.
from api.user.models import CustomUser
class Usercart(models.Model):
    pass
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity=models.IntegerField()
    selectedProductColor=models.CharField(max_length=50)
    selectedProductSize=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add = True)
    updated_at=models.DateTimeField(auto_now = True)
    def __str__(self) :
        return self.user.name