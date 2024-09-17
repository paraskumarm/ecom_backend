from rest_framework import serializers

from api.product.serializers import ProductSerializer

from .models import OrderPayTm

class OrderPayTmSerializer(serializers.HyperlinkedModelSerializer):
    # product=ProductSerializer(read_only=True)
    class Meta:
        model=OrderPayTm
        fields="__all__"
        depth=3