from api.address.serializers import AddressSerializer
from rest_framework import viewsets
from django.http import JsonResponse
from .serializers import AddressSerializer
from .models import Address
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import Address
from django.contrib.auth import get_user_model
class AddressViewSet(viewsets.ModelViewSet):
    queryset=Address.objects.all().order_by('id')
    serializer_class=AddressSerializer

@csrf_exempt
def add(request, id):
    # return JsonResponse({'msg': 'HI'})

    if request.method == "POST":
        user_id = id
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        street_address = request.POST['street_address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        phone = request.POST['phone']
        email = request.POST['email']
        

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})

        address = Address(user=user,first_name=first_name,last_name=last_name,street_address=street_address,city=city,state=state,pincode=pincode,phone=phone,email=email)
        address.save()
        
        return JsonResponse({'success': True, 'error': False, 'msg': 'Address stored Successfully','address_id':address.pk})