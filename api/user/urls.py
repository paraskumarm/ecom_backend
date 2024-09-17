# this file is added manually
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()  # changed from simple router to default router
router.register(r"", views.UserViewSet)
urlpatterns = [
    path("login/", views.signin, name="signin"),
    path("googlelogin/", views.googlesignin, name="googlesignin"),
    path("logout/<int:id>/", views.signout, name="signout"),
    path("", include(router.urls)),
]
