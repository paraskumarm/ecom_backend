
from rest_framework import serializers
from .models import Slider


class SliderSerializer(serializers.HyperlinkedModelSerializer):
    image=serializers.ImageField(max_length=None,allow_empty_file=False,allow_null=True,required=False)
    class Meta:
        model = Slider
        fields=('id','title','subtitle','text','image')
      

