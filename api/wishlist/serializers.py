#added this file manually
from django.db.models import fields
from api.wishlist.models import Wishlist
from rest_framework import serializers

from api.product.serializers import ProductSerializer


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    product=ProductSerializer(read_only=True)
    class Meta:
        model=Wishlist
        fields=('id','product')
        depth=3