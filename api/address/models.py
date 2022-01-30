from django.db import models
from api.user.models import CustomUser
# Create your models here.
class Address(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    street_address=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    state=models.CharField(max_length=200)
    pincode=models.CharField(max_length=6)
    phone=models.CharField(max_length=10)
    email=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add = True)
    updated_at=models.DateTimeField(auto_now = True)
