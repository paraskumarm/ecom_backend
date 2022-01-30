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
def add(request, user_id,token,product_id):
    # return JsonResponse({'msg': 'HI'})
    if not validate_user_session(user_id, token):
        return JsonResponse({'error': 'Please re-login', 'code': '1'})
    if request.method == "POST":
        user_id = id
        quantity = request.POST['quantity']
        selectedProductColor = request.POST['selectedProductColor']
        selectedProductSize = request.POST['selectedProductSize']
        product_id = request.POST['product_id']
        print("id===",product_id)
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'})
        cart = Usercart(user=user,product=product,selectedProductColor=selectedProductColor,selectedProductSize=selectedProductSize,quantity=quantity)
        cart.save()
    
    return JsonResponse({'success': True, 'error': False, 'cart': cart})