from rest_framework import serializers
from api.product.serializers import ProductSerializer
from .models import OrderCOD


class OrderCODSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderCOD
        fields = "__all__"
        depth = 3
