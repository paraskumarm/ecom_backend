
from itertools import product
import json
from django.http import JsonResponse
import Google
from api.product.models import Product
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.orderPayTm.models import OrderPayTm,Address
from django.contrib.auth import get_user_model

from api.order.models import Order
from . import Checksum
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
from backend.settings import CONFIG_DIR

config = configparser.ConfigParser(interpolation=None)
config.read_file(open(CONFIG_DIR))

MERCHANTID = config.get('PAYTM','MERCHANTID')
MERCHANTKEY = config.get('PAYTM','MERCHANTKEY')
SEND_TO = [email.strip() for email in config.get('EMAIL','SEND_TO').split(',')]
CALLBACK_URL = config.get('PAYTM','CALLBACK_URL')

def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False
# @csrf_exempt
@api_view(['POST'])
def start_payment(request,user_id,token,address_id):
    # request.data is coming from frontend
    if not validate_user_session(user_id, token):
        return JsonResponse({'error': 'Please re-login', 'code': '1'})
    if request.method == "POST":
        user_id = user_id
        address_id=address_id
        product_names = request.POST['product_names']
        total_products = request.POST['total_products']
        total_amount = request.POST['total_amount']
        pkarr = request.POST['pkarr']
        quantity_info = request.POST['quantity_info']
        color_info = request.POST['color_info']
        size_info = request.POST['size_info']
        status_info = request.POST['status_info']
        pkarrqty = request.POST['pkarrqty']
        product_name_array = request.POST['product_name_array']
        price_info = request.POST['price_info']
        product_id = request.POST['product_id']
        
        pkarr=json.loads(pkarr)
        quantity_info=json.loads(quantity_info)
        color_info=json.loads(color_info) 
        size_info=json.loads(size_info)
        pkarrqty=json.loads(pkarrqty)
        product_name_array=json.loads(product_name_array)
        price_info=json.loads(price_info)
        product_id=json.loads(product_id)
        for i in pkarr:
            i=int(i)
        list1=pkarr
        list1,quantity_info = zip(*sorted(zip(list1,quantity_info)))
        list1=pkarr
        list1,color_info = zip(*sorted(zip(list1,color_info)))
        list1=pkarr
        list1,size_info = zip(*sorted(zip(list1,size_info)))
        list1=pkarr
        list1,product_name_array = zip(*sorted(zip(list1,product_name_array)))
        list1=pkarr
        list1,price_info = zip(*sorted(zip(list1,price_info)))
        list1=pkarr
        list1,product_id = zip(*sorted(zip(list1,product_id)))
        # list1=pkarr
        # list1,size_info = zip(*sorted(zip(list1,size_info)))

        

        
        UserModel = get_user_model()
        
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return JsonResponse({'error': 'Address does not exist'})
        try:
            products = Product.objects.filter(pk__in=pkarr)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'product does not exist'})
        order = OrderPayTm(user=user,address=address,product_names=product_names,total_products=total_products,total_amount=total_amount,quantity_info=quantity_info,size_info=size_info,color_info=color_info,status_info=status_info,pkarrqty=pkarrqty)
        order.save()
        order.products.set(products)
        order.save()
        # Order
        print("pid=",product_id)
        print("size_info=",size_info)
        print("price_info=",price_info)
        print("status_info=",status_info)
        for i in range (0,len(color_info)):
          orderhistory = Order(transaction_id=order.pk,user=user,product=Product.objects.get(pk=product_id[i]),address=address,product_name=product_name_array[i],total_amount=price_info[i],quantity_info=quantity_info[i],size_info=size_info[i],color_info=color_info[i],status_info="Order Received")
          orderhistory.save()

    # we have to send the param_dict to the frontend
    # these credentials will be passed to paytm order processor to verify the business account
   
    param_dict = {
        'MID': MERCHANTID,
        'ORDER_ID': str(order.pk),
        'TXN_AMOUNT': str(total_amount),
        'CUST_ID': str(user.email),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': CALLBACK_URL+user.email+"/",
        # 'CALLBACK_URL': "http://127.0.0.1:8000/api/paytmGateway/handlepayment/"
        # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
    }

    # create new checksum (unique hashed string) using our merchant key with every paytm payment
    param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANTKEY)
    # send the dictionary with all the credentials to the frontend
    return Response({'param_dict': param_dict})


@api_view(['POST'])
def handlepayment(request,user_mailid):
    checksum = ""
   
    # the request.POST is coming from paytm
    form = request.POST
    
    response_dict = {}
    order = None  # initialize the order varible with None
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            checksum = form[i]

        if i == 'ORDERID':
            # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
            order = OrderPayTm.objects.get(id=form[i])

    
    # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
    verify = Checksum.verify_checksum(response_dict, MERCHANTKEY, checksum)
    CLIENT_SECRET_FILE = 'client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    if verify:
        if response_dict['RESPCODE'] == '01':
            # if the response code is 01 that means our transaction is successfull
            print('order successful')
            # after successfull payment we will make isPaid=True and will save the order
            order.isPaid = True
            order.save()
            # we will render a template to display the payment status

            for email_id in SEND_TO:
                emailMsg = 'Order of ₹' + form['TXNAMOUNT'] + ' is successful having order id ' + form['ORDERID']
                mimeMessage = MIMEMultipart()
                mimeMessage['to'] = email_id
                mimeMessage['subject'] = 'Gmail API Test ' + form['STATUS']
                mimeMessage.attach(MIMEText(emailMsg, 'plain'))
                raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
                message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
                print("EMAIL SENT TO:",email_id)

            return render(request, 'transaction_response.html', {'response': response_dict})
        else:
            failed_orders=Order.objects.filter(transaction_id=order.pk)
            failed_orders.delete()
            print("all_deleted")

            print('order was not successful because' + response_dict['RESPMSG'])
            for email_id in SEND_TO:
                emailMsg = 'Order of ₹' + form['TXNAMOUNT'] + ' is failed having order id ' + form['ORDERID']
                mimeMessage = MIMEMultipart()
                mimeMessage['to'] = email_id
                mimeMessage['subject'] = 'Gmail API Test ' + form['STATUS']
                mimeMessage.attach(MIMEText(emailMsg, 'plain'))
                raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
                message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
                print("EMAIL SENT TO:",email_id)
                
            order.delete()
            return render(request, 'transaction_response.html', {'response': response_dict})
