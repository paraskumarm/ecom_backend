from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework import viewsets

from api.product.models import Product

from .serializers import WishlistSerializer
from .models import Wishlist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

# Create your views here.
class WishlistViewSet(viewsets.ModelViewSet):
    queryset=Wishlist.objects.all().order_by('id')
    serializer_class=WishlistSerializer
    filterset_fields=['user']

def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False
@csrf_exempt
def add(request, user_id,token):
    # return JsonResponse({'msg': 'HI'})
    # print("request==",request.POST)
    print("requset end here")
    if not validate_user_session(user_id, token):
        return JsonResponse({'error': 'Please re-login', 'code': '1'})
    if request.method == "POST":
        user_id = user_id
        product_id = (request.POST['product_id'])
        print(product_id)
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})
        try:
            product = Product.objects.get(pk=int(product_id))
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'})
            # i have to check if product is already present in the given usercart or not
        try:
            previouscart=Wishlist.objects.get(user=user_id,product=int(product_id))
            previouscart.save()
            return JsonResponse({'success': True, 'error': False,'id':previouscart.pk})
            
        except Wishlist.DoesNotExist:
            cart=Wishlist(user=user,product=product)
            cart.save()
            return JsonResponse({'success': True, 'error': False,'id':cart.pk})
def deleteall(request,user_id):
    try:
        cart=Wishlist.objects.all().filter(user=user_id)
        cart.delete()
        return JsonResponse({'success': True, 'error': False})
    except Wishlist.DoesNotExist:
        return JsonResponse({'error': 'Cart does not exist'})

            