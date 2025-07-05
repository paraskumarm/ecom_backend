from rest_framework import serializers

from .models import OrderPayTm


class OrderPayTmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderPayTm
        fields = "__all__"
        depth = 3
