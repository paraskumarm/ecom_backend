from rest_framework import serializers

from api.product.serializers import ProductSerializer
from api.usercart.models import Usercart


class CartSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Usercart
        fields = (
            "id",
            "product",
            "quantity",
            "selectedProductColor",
            "selectedProductSize",
        )
        depth = 3
