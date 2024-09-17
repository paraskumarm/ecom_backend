from django.urls import path

from api.paytmGateway.views import start_payment
from api.paytmGateway.views import handlepayment

urlpatterns = [
    path(
        "pay/<int:user_id>/<str:token>/<int:address_id>/",
        start_payment,
        name="start_payment",
    ),
    path("handlepayment/<str:user_mailid>/", handlepayment, name="handlepayment"),
]
