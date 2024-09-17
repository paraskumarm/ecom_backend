from rest_framework import serializers
from .models import Product, Variation  # ,Images#,Tags,Category

# class TagSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Tags
#         fields=('tag')
# class CategorySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Category
#         fields=('category')


# class SizeSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Size
#         fields=('name','stock')
class VariationSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False
    )

    class Meta:
        model = Variation
        fields = ("color", "image", "size")
        depth = 1


# class ImagesSerializer(serializers.HyperlinkedModelSerializer):
#     image=serializers.ImageField(max_length=None,allow_empty_file=False,allow_null=True,required=False)
#     class Meta:
#         model = Images
#         fields=('image')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    # image=serializers.ImageField(max_length=None,allow_empty_file=False,allow_null=True,required=False)
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
