from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.OrderPayTmViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path(
        "add/<int:user_id>/<str:token>/<int:address_id>/",
        views.add,
        name="orderPayTm.add",
    ),
]
