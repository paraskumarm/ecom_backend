from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.shortcuts import render
from .serializers import SliderSerializer

from .models import Slider

# Create your views here.
class SliderViewSet(viewsets.ModelViewSet):
    queryset=Slider.objects.all()
    serializer_class=SliderSerializer



