from rest_framework import viewsets
from django.shortcuts import render
from .serializers import ProductSerializer, VariationSerializer#,ImagesSerializer#,TagSerializer,CategorySerializer

from .models import Product, Variation#,Images#,Tags,Category

# Create your views here.
class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
class VariationViewSet(viewsets.ModelViewSet):
    queryset=Variation.objects.all()
    serializer_class=VariationSerializer
# class SizeViewSet(viewsets.ModelViewSet):
#     queryset=Size.objects.all()
#     serializer_class=SizeSerializer
# class ImagesViewSet(viewsets.ModelViewSet):
#     queryset=Images.objects.all()
#     serializer_class=ImagesSerializer
# class TagViewSet(viewsets.ModelViewSet):
#     queryset=Tags.objects.all()
#     serializer_class=TagSerializer
# class CategoryViewSet(viewsets.ModelViewSet):
#     queryset=Category.objects.all()
#     serializer_class=CategorySerializer


