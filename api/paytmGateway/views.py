import base64
import configparser
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import razorpay
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory

import Google
from api.order.models import Order
from api.orderCOD.models import OrderCOD
from api.orderPayTm.models import Address, OrderPayTm
from api.orderPayTm.serializers import OrderPayTmSerializer
from api.product.models import Product
from backend.settings import CONFIG_DIR

# import PaytmChecksum
config = configparser.ConfigParser(interpolation=None)
config.read_file(open(CONFIG_DIR))

MERCHANTID = config.get("RAZORPAY", "MERCHANTID")
MERCHANTKEY = config.get("RAZORPAY", "MERCHANTKEY")
SEND_TO = [email.strip() for email in config.get("EMAIL", "SEND_TO").split(",")]


def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@api_view(["POST"])
def start_payment(request, user_id, token, address_id):
    if not validate_user_session(user_id, token):
        return JsonResponse({"error": "Please re-login", "code": "1"})
    if request.method == "POST":
        user_id = user_id
        address_id = address_id
        product_names = request.POST["product_names"]
        total_products = request.POST["total_products"]
        total_amount = request.POST["total_amount"]
        quantity_info = request.POST["quantity_info"]
        color_info = request.POST["color_info"]
        size_info = request.POST["size_info"]
        status_info = request.POST["status_info"]
        product_name_array = request.POST["product_name_array"]
        price_info = request.POST["price_info"]
        product_id = request.POST["product_id"]
        quantity_info = json.loads(quantity_info)
        color_info = json.loads(color_info)
        size_info = json.loads(size_info)
        product_name_array = json.loads(product_name_array)
        price_info = json.loads(price_info)
        product_id = json.loads(product_id)

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({"error": "User does not exist"})
        try:
            address = Address.objects.get(pk=address_id)
        except Address.DoesNotExist:
            return JsonResponse({"error": "Address does not exist"})
        try:
            products = Product.objects.filter(pk__in=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"error": "product does not exist"})

        # Order
        transaction_id = OrderCOD.objects.count() + OrderPayTm.objects.count() + 1
        for i in range(0, len(color_info)):
            orderhistory = Order(
                transaction_id=transaction_id,
                user=user,
                product=Product.objects.get(pk=product_id[i]),
                address=address,
                product_name=product_name_array[i],
                total_amount=price_info[i],
                quantity_info=quantity_info[i],
                size_info=size_info[i],
                color_info=color_info[i],
                status_info="Order Received",
            )
            orderhistory.save()
        isCOD = 0
        # HANDLE COD AND PAYTM (isCOD==1 OR isCOD==0)
        if isCOD == 1:
            order = OrderCOD(
                user=user,
                address=address,
                product_names=product_names,
                total_products=total_products,
                total_amount=total_amount,
                transaction_id=transaction_id,
            )
            order.save()
            order.products.set(products)
            order.save()
            # return render(request, 'transaction_response.html')
            return JsonResponse({"param_dict": {}})
        else:
            print(MERCHANTID, " ", MERCHANTKEY)
            client = razorpay.Client(auth=(MERCHANTID, MERCHANTKEY))
            payment = client.order.create(
                {
                    "amount": int(total_amount) * 100,
                    "currency": "INR",
                    "payment_capture": "1",
                }
            )
            order = OrderPayTm(
                user=user,
                address=address,
                product_names=product_names,
                total_products=total_products,
                total_amount=total_amount,
                transaction_id=transaction_id,
                order_payment_id=payment["id"],
            )
            order.save()
            order.products.set(products)
            order.save()
            factory = APIRequestFactory()
            request = factory.get("/")
            serializer = OrderPayTmSerializer(
                instance=order, context={"request": Request(request)}
            )

            data = {
                "payment": payment,
                "order": serializer.data,
                "user_mailid": user.email,
            }
            # send the dictionary with all the credentials to the frontend
            return Response(data)


@api_view(["POST"])
def handlepayment(request, user_mailid):
    res = json.loads(request.data["response"])
    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    for i in res.keys():
        if i == "razorpay_order_id":
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            ord_id = res[i]

        if i == "razorpay_payment_id":
            # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
            raz_pay_id = res[i]

        if i == "razorpay_signature":
            raz_signature = res[i]

    # get order by payment_id which we've created earlier with isPaid=False
    order = OrderPayTm.objects.get(order_payment_id=ord_id)

    data = {
        "razorpay_order_id": ord_id,
        "razorpay_payment_id": raz_pay_id,
        "razorpay_signature": raz_signature,
    }
    client = razorpay.Client(auth=(MERCHANTID, MERCHANTKEY))

    check = client.utility.verify_payment_signature(data)
    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = ["https://mail.google.com/"]
    service = Google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    if check == False:
        failed_orders = Order.objects.filter(transaction_id=order.pk)
        failed_orders.delete()

        for email_id in SEND_TO:
            emailMsg = "Order of ₹" + (str)(order.total_amount) + " is failed"
            mimeMessage = MIMEMultipart()
            mimeMessage["to"] = email_id
            mimeMessage["subject"] = "DARZI WARZI-PAYMENT FAILED"
            mimeMessage.attach(MIMEText(emailMsg, "plain"))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = (
                service.users()
                .messages()
                .send(userId="me", body={"raw": raw_string})
                .execute()
            )

        order.delete()
        return JsonResponse({"error": "Something went wrong"})
    else:
        for email_id in SEND_TO:
            emailMsg = (
                "Order of ₹"
                + (str)(order.total_amount)
                + " is successful having order id "
                + (str)(order.id)
            )
            mimeMessage = MIMEMultipart()
            mimeMessage["to"] = email_id
            mimeMessage["subject"] = "DARZI WARZI-PAYMENT SUCCESSFUL"
            mimeMessage.attach(MIMEText(emailMsg, "plain"))
            raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
            message = (
                service.users()
                .messages()
                .send(userId="me", body={"raw": raw_string})
                .execute()
            )

        order.isPaid = True
        order.save()

        res_data = {"message": "payment successfully received!"}
        return JsonResponse(res_data)
