from urllib import request
from django.http import JsonResponse
from django.shortcuts import render
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import configparser
from backend.settings import CONFIG_DIR
import Google
from django.views.decorators.csrf import csrf_exempt

config = configparser.ConfigParser(interpolation=None)
config.read_file(open(CONFIG_DIR))

SEND_TO = [email.strip() for email in config.get("EMAIL", "SEND_TO").split(",")]



@csrf_exempt
def sendmail(request):
    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME = "gmail"
    API_VERSION = "v1"
    SCOPES = ["https://mail.google.com/"]

    service = Google.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    name = request.POST["name"]
    email = request.POST["email"]
    subject = request.POST["subject"]
    msg = request.POST["msg"]

    for email_id in SEND_TO:
        emailMsg = "name " + name + " email " + email + " messsage is " + msg
        mimeMessage = MIMEMultipart()
        mimeMessage["to"] = email_id
        mimeMessage["subject"] = subject
        mimeMessage.attach(MIMEText(emailMsg, "plain"))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()
        service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
        print("EMAIL SENT TO:", email_id)

    return JsonResponse({"msg": "email sent"})
