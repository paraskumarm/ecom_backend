#this file is added manually
from django.urls import path,include
from . import views
from rest_framework import routers

urlpatterns =[
    path('sendmail/',views.sendmail,name='sendmail')
]
