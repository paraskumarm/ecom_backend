from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.CartViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("addtocart/<int:user_id>/<str:token>/", views.add, name="cart.add"),
    path("deleteall/<int:user_id>/", views.deleteall, name="cart.deleteall"),
    path("decrease/<int:user_id>/<int:cart_id>/", views.decrease, name="cart.decrease"),
]
