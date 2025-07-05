import random
import re

from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import UserSerializer


def generate_session_token(length=10):
    arr = []
    for i in range(0, 26):
        arr.append(chr(i + 97))
    for i in range(10):
        arr.append(str(i))
    s = ""
    for i in range(length):
        s += random.SystemRandom().choice(arr)
    return s


@csrf_exempt
def signin(request):
    if not request.method == "POST":
        return JsonResponse({"error": "Send a post request with a valid parameter"})
    username = request.POST["email"]
    password = request.POST["password"]

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({"error": "Enter a valid email"})

    if len(password) < 5:
        return JsonResponse({"error": "Password need to be of atleast 5 character"})
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)
        if user.check_password(password):
            usr_dict = UserModel.objects.filter(email=username).values().first()
            usr_dict.pop("password")
            if user.session_token != "0":
                user.session_token = "0"
                user.save()
                return JsonResponse({"error": "Previous session exists"})
            token = generate_session_token()
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({"token": token, "user": usr_dict})
        else:
            return JsonResponse({"error": "Invalid Password"})
    except UserModel.DoesNotExist:
        return JsonResponse({"error": "Invalid email"})


@csrf_exempt
def googlesignin(request):
    if not request.method == "POST":
        return JsonResponse({"error": "Send a post request with a valid parameter"})

    name = request.POST["name"]
    username = request.POST["email"]
    token = request.POST["token"]

    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=username)
        usr_dict = UserModel.objects.filter(email=username).values().first()

        if user.session_token != "0":
            user.session_token = "0"
            user.save()
            return JsonResponse({"error": "Previous session exists"})

        user.session_token = token
        user.save()
        login(request, user)
        return JsonResponse({"token": token, "user": usr_dict})
    except UserModel.DoesNotExist:
        dict = {"name": name, "email": username, "password": None}
        UserSerializer().create(dict)
        usr_dict = UserModel.objects.filter(email=username).values().first()
        return JsonResponse({"token": token, "user": usr_dict})


def signout(request, id):
    logout(request)
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({"error": "Invalid user ID"})
    return JsonResponse({"success": "Logout success"})


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations on the CustomUser model.

    This viewset extends Django Rest Framework's ModelViewSet to provide
    default implementations for standard actions (list, create, retrieve,
    update, partial_update, destroy) on the CustomUser model. It supports
    custom permission classes per action via the `permission_classes_by_action`
    attribute.

    Attributes:
        permission_classes_by_action (dict): Maps action names to lists of permission classes.
            For example, {"create": [AllowAny]} allows unrestricted access to the create action.
        queryset (QuerySet): The queryset of CustomUser objects, ordered by 'id'.
        serializer_class (Serializer): The serializer class used for CustomUser objects.

    Methods:
        get_permissions():
            Returns the list of permission instances that should be used for the current action.
            Tries to retrieve permission classes from `permission_classes_by_action` for the
            current action; if not found, falls back to the default `permission_classes`.
    """

    permission_classes_by_action = {"create": [AllowAny]}
    queryset = CustomUser.objects.all().order_by("id")
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]
