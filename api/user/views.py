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
from django.contrib.auth import login,logout
# Create your views here.
import random
import re

def generate_session_token(length=10):
    return ''.join(random.SystemRandom().choice([chr(i)for i in range(97,123)]+[str(i) for i in range(10)]) for _ in range(length) )
 
@csrf_exempt

def signin(request):
    if not request.method =='POST':
        return JsonResponse({'error':'Send a post request with a valid parameter'}) 
    username=request.POST['email']
    password=request.POST['password']

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$",username):
        return JsonResponse({'error':'Enter a valid email'})
    
    if len(password)<5:
        return JsonResponse({'error':'Password need to be of atleast 5 character'})
    UserModel=get_user_model()

    try:
        user=UserModel.objects.get(email=username)
        if user.check_password(password):
            usr_dict=UserModel.objects.filter(email=username).values().first()
            usr_dict.pop('password')

            if user.session_token!="0":
                user.session_token="0"
                user.save()
                return JsonResponse({'error':'Previous session exists'})
            token=generate_session_token()
            user.session_token=token
            user.save()
            login(request,user)
            return JsonResponse({'token':token,'user':usr_dict})
        else:
            return JsonResponse({'error':'Invalid Password'})
    except UserModel.DoesNotExist:
        return JsonResponse({'error':'Invalid email'})
@csrf_exempt
def googlesignin(request):
    # send email and token
    print("paras",request.POST)
    if not request.method =='POST':
        return JsonResponse({'error':'Send a post request with a valid parameter'}) 
    
    name=request.POST['name']
    username=request.POST['email']
    token=request.POST['token']
    # print(token)
    UserModel=get_user_model()
    # token=generate_session_token()
    try:
        # if user exists
        # get email,get token,no password required,password is none
        user=UserModel.objects.get(email=username)
        usr_dict=UserModel.objects.filter(email=username).values().first()
        # usr_dict.pop('password')

        if user.session_token!="0":
            # logout if already signed in
            user.session_token="0"
            user.save()
            return JsonResponse({'error':'Previous session exists'})
        
        user.session_token=token #store token sent by google
        user.save()
        login(request,user)
        return JsonResponse({'token':token,'user':usr_dict})
    except UserModel.DoesNotExist:
        # create user by name email phone
        # save user
        dict={"name":name,"email":username,"password":None}
        print(dict)
        UserSerializer().create(dict)#doubt
        usr_dict=UserModel.objects.filter(email=username).values().first()
        return JsonResponse({'token':token,'user':usr_dict})

def signout(request, id):
    logout(request)
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        user.session_token = "0"
        user.save()
    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid user ID'})
    return JsonResponse({'success': 'Logout success'})
    
class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes] 