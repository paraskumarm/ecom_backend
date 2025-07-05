from rest_framework import serializers

from .models import Product, Variation


class VariationSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False
    )

    class Meta:
        model = Variation
        fields = ("color", "image", "size")
        depth = 1


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "discount",
            "offerEnd",
            "new",
            "saleCount",
            "category",
            "tag",
            "variation",
            "image1",
            "image2",
            "image3",
            "image4",
            "image5",
            "shortDescription",
            "fullDescription",
        )
        depth = 2
