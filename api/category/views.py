from api.category.serializers import CategorySerializer
from rest_framework import viewsets
from .serializers import CategorySerializer
from .models import Category
# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all().order_by('id')
    serializer_class=CategorySerializer