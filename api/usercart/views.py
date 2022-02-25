from django.http import JsonResponse
from rest_framework import viewsets

from api.product.models import Product

from .serializers import CartSerializer
from .models import Usercart
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

# Create your views here.
class CartViewSet(viewsets.ModelViewSet):
    queryset=Usercart.objects.all().order_by('id')
    serializer_class=CartSerializer
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



    print("called")
    if not validate_user_session(user_id, token):
        return JsonResponse({'error': 'Please re-login', 'code': '1'})
    if request.method == "POST":
        user_id = user_id
        # print(request.POST)
        quantity = request.POST['quantity']
        selectedProductColor = request.POST['selectedProductColor']
        selectedProductSize = request.POST['selectedProductSize']
        product_id = (request.POST['product_id'])
        # print("id===",product_id)
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
        print("qty=",quantity)
        print("selectedProductColor=",selectedProductColor)
        print("selectedProductSize=",selectedProductSize)
        try:
            previouscart=Usercart.objects.get(user=user_id,product=int(product_id),selectedProductSize=selectedProductSize)
            previouscart.quantity=previouscart.quantity+int(quantity)
            previouscart.save()
            return JsonResponse({'success': True, 'error': False,'id':previouscart.pk})
            
            # print("end")
        except Usercart.DoesNotExist:
            cart = Usercart(user=user,product=product,selectedProductColor=selectedProductColor,selectedProductSize=selectedProductSize,quantity=int(quantity))
            cart.save()
            return JsonResponse({'success': True, 'error': False,'id':cart.pk})
def deleteall(request,user_id):
    try:
        cart=Usercart.objects.all().filter(user=user_id)
        print(cart)
        cart.delete()
        return JsonResponse({'success': True, 'error': False})
    except Usercart.DoesNotExist:
        return JsonResponse({'error': 'Cart does not exist'})

            
def decrease(request, user_id,cart_id):
    
    print(user_id,cart_id)
    try:
        previouscart=Usercart.objects.get(id=cart_id)
        previouscart.quantity=previouscart.quantity-1
        if previouscart.quantity==0:
            previouscart.delete()
        else:
            previouscart.save()
        # print("end")
        return JsonResponse({'success': True, 'error': False,'id':previouscart.pk})
    except Usercart.DoesNotExist:
        return JsonResponse({'success': False, 'error': True})