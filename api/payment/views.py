from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators import csrf
from django.views.decorators.csrf import csrf_exempt
import braintree
# Create your views here.

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="q737rkbh9hy7rsmw",
        public_key="dh5tcqkbpbk4qc5h",
        private_key="43d240082a7eb278c2c09b55a5d33b77"
    )
)
def validate_user_session(id,token):
    UserModel=get_user_model()
    try:
        user=UserModel.objects.get(pk=id)
        if user.session_token ==token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False
@csrf_exempt
def generate_token(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid session,Please login again'})
    return JsonResponse({'clientToken':gateway.client_token.generate(),'success':True})
@csrf_exempt
def process_payment(request,id,token):
    if not validate_user_session(id,token):
        return JsonResponse({'error':'Invalid session,Please login again'})
    nonce_from_the_client=request.POST["paymentMethodNonce"]
    amount_from_the_client=request.POST["amount"]
    print("RESULT=",nonce_from_the_client,amount_from_the_client)
    result=gateway.transaction.sale({
        "amount":amount_from_the_client,
        "payment_method_nonce":nonce_from_the_client,
        "options":{
            "submit_for_settlement":True
        }
    })
    
    if result.is_success:
        return JsonResponse({"success":result.is_success,"transaction":{'id':result.transaction.id,'amount':result.transaction.amount}})
    else:
        print("YOYOYOOYOY")
        print(result.message)
        print(result.params)
        return JsonResponse({"error":True,'success':False})