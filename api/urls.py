# added mannualy
# from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken import views
from .views import home
urlpatterns = [
    path('', home,name="home"),
    path('category/', include('api.category.urls')),
    path('product/', include('api.product.urls')),
    path('user/', include('api.user.urls')),
    path('order/', include('api.order.urls')),
    path('slider/', include('api.slider.urls')),
    path('payment/', include('api.payment.urls')),
    path('paytmGateway/', include('api.paytmGateway.urls')),
    path('orderPayTm/', include('api.orderPayTm.urls')),
    path('address/', include('api.address.urls')),
    path('usercart/', include('api.usercart.urls')),
    path('api-token-auth/',views.obtain_auth_token,name='api_token_auth'),#not needed we can remove
]
