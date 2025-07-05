from django.urls import include, path
from rest_framework.authtoken import views

from .views import home

urlpatterns = [
    path("", home, name="home"),
    path("product/", include("api.product.urls")),
    path("user/", include("api.user.urls")),
    path("orderhistory/", include("api.order.urls")),
    path("paytmGateway/", include("api.paytmGateway.urls")),
    path("orderPayTm/", include("api.orderPayTm.urls")),
    path("address/", include("api.address.urls")),
    path("usercart/", include("api.usercart.urls")),
    path("wishlist/", include("api.wishlist.urls")),
    path("mail/", include("api.mailing.urls")),
    path(
        "api-token-auth/", views.obtain_auth_token, name="api_token_auth"
    ),  # not needed we can remove
]
