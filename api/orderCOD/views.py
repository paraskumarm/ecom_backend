from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from api.orderCOD.serializers import OrderCODSerializer

from .models import Address, OrderCOD


class OrderCODViewSet(viewsets.ModelViewSet):
    queryset = OrderCOD.objects.all()
    serializer_class = OrderCODSerializer
    filterset_fields = ["user"]


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
def add(request, user_id, token, address_id):
    # return JsonResponse({'msg': 'HI'})
    if not validate_user_session(user_id, token):
        return JsonResponse({"error": "Please re-login", "code": "1"})
    if request.method == "POST":
        user_id = user_id
        address_id = address_id
        product_names = request.POST["product_names"]
        total_products = request.POST["total_products"]
        total_amount = request.POST["total_amount"]

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({"error": "User does not exist"})
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Address does not exist"})
        order = OrderCOD(
            user=user,
            address=address,
            product_names=product_names,
            total_products=total_products,
            total_amount=total_amount,
        )
        order.save()

        return JsonResponse(
            {
                "success": True,
                "error": False,
                "msg": "Ordered Successfully",
                "order_id": order.pk,
            }
        )
