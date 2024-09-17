import abc
from genericpath import exists
from django.contrib.auth.backends import UserModel
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout

# Create your views here.
import random
import re


def generate_session_token(length=10):
    arr = []
    for i in range(0, 26):
        arr.append(chr(i + 97))
    for i in range(10):
        arr.append(str(i))
    s = ""
    for i in range(10):
        s += random.SystemRandom().choice(arr)
    return s


@csrf_exempt  # as we are making request from other origin
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
            # This method takes a plaintext password as an argument, and then it hashes it using the same algorithm and salt used to hash the password during the registration or set_password process. It then compares the hashed password to the stored hash and returns True if they match and False if they don't.
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
    # send email and token
    print("paras", request.POST)
    if not request.method == "POST":
        return JsonResponse({"error": "Send a post request with a valid parameter"})

    name = request.POST["name"]
    username = request.POST["email"]
    token = request.POST["token"]
    # print(token)
    UserModel = get_user_model()
    # token=generate_session_token()
    try:
        # if user exists
        # get email,get token,no password required,password is none
        user = UserModel.objects.get(email=username)
        usr_dict = UserModel.objects.filter(email=username).values().first()
        # usr_dict.pop('password')

        if user.session_token != "0":
            # logout if already signed in
            user.session_token = "0"
            user.save()
            return JsonResponse({"error": "Previous session exists"})

        user.session_token = token  # store token sent by google
        user.save()
        login(request, user)
        return JsonResponse({"token": token, "user": usr_dict})
    except UserModel.DoesNotExist:
        # create user by name email phone
        # save user
        dict = {"name": name, "email": username, "password": None}
        print(dict)
        UserSerializer().create(dict)  # doubt
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

    #  this UserViewSet class is a generic view set provided by Django Rest Framework (DRF) that handles CRUD operations for the CustomUser model with the ability to set different permission classes for different actions, and order the queryset by id.

    #  The get_permissions method is overridden to return the permission classes that should be used for the current action. It first tries to retrieve the permission classes for the current action from the permission_classes_by_action dictionary, and if that fails, it falls back to the permission_classes attribute.
