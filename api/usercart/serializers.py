#added this file manually
from django.db.models import fields
from api.usercart.models import Usercart
from rest_framework import serializers

from api.product.serializers import ProductSerializer


class CartSerializer(serializers.HyperlinkedModelSerializer):
    # product=ProductSerializer(read_only=True)
    class Meta:
        model=Usercart
        fields=('id','product','quantity','selectedProductColor','selectedProductSize')
        depth=3