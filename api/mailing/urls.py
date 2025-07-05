from django.urls import include, path

from . import views

urlpatterns = [path("sendmail/", views.sendmail, name="sendmail")]
