"""URL configuration for the address API."""

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.AddressViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("add/<int:id>/", views.add, name="address.add"),
]
