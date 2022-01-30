#this file is added manually
from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()#changed from simple router to default router
router.register(r'',views.SliderViewSet)
urlpatterns =[
    path('',include(router.urls))
]
