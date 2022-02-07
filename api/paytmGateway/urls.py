from django.urls import path

from api.paytmGateway.views import start_payment
from api.paytmGateway.views import handlepayment

# from api.paytmGateway import views


urlpatterns = [
    path('pay/<int:user_id>/<str:token>/<int:address_id>/', start_payment, name="start_payment"),
    path('handlepayment/', handlepayment, name="handlepayment"),
]