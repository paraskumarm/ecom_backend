from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.ProductViewSet)
router.register(r"", views.VariationViewSet)

urlpatterns = [path("", include(router.urls))]
