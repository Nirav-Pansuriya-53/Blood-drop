from django.conf import settings
import requests
import json

def send_sms(phone_numbers, message):

    querystring = {"authorization":settings.FAST_SMS_KEY,"message":message,"language":"english","route":"q","numbers":",".join(phone_numbers)}

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.request("GET", settings.FAST_SMS_URL, headers=headers, params=querystring)

    return json.loads(response.content)
