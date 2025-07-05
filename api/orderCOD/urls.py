# this file is added manually
from django.urls import include, path
from rest_framework import routers

from . import views

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
