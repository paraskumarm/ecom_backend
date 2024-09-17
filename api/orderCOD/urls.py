# this file is added manually
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.OrderCODViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path(
        "add/<int:user_id>/<str:token>/<int:address_id>/",
        views.add,
        name="orderCOD.add",
    ),
]
