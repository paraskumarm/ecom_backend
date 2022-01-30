#added this file manually
from django.db.models import fields
from api.category.models import Category
from rest_framework import serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Category
        fields=('id','name','description')