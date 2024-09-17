from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"", views.WishlistViewSet)
urlpatterns = [
    path("", include(router.urls)),
    path("addtowishlist/<int:user_id>/<str:token>/", views.add, name="wishlist.add"),
    path(
        "deleteallwishlist/<int:user_id>/", views.deleteall, name="wishlist.deleteall"
    ),
]
