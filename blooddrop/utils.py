from django.conf import settings
import requests
import json

def send_sms(phone_numbers, message):

    querystring = {"authorization":settings.FAST2SMS_API_KEY,"sender_id":"FTWSMS", "message":message,"language":"english","route":"q","numbers":phone_numbers}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", settings.FAST_SMS_URL, headers=headers, params=querystring)

    print("*"*100)
    print(json.loads(response.content))
    print("*"*100)
 