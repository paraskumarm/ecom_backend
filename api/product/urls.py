#this file is added manually
from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()#changed from simple router to default router
router.register(r'',views.ProductViewSet)
router.register(r'',views.VariationViewSet)
router.register(r'',views.SizeViewSet)
router.register(r'',views.ImagesViewSet)
# router.register(r'',views.TagViewSet)
# router.register(r'',views.CategoryViewSet)


urlpatterns =[
    path('',include(router.urls))
]
