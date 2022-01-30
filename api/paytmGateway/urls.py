from django.urls import path

from api.paytmGateway import views

urlpatterns = [
    path('pay/<int:user_id>/<str:token>/<int:address_id>/', views.start_payment, name="start_payment"),
    path('handlepayment/', views.handlepayment, name="handlepayment"),
]