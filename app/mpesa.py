from app import app
import requests
from requests.auth import HTTPBasicAuth
from flask import json
from datetime import datetime
import base64


class MpesaC2BCredential:
    consumer_key = app.config['MPESA_CONSUMER_KEY']
    consumer_secret = app.config["MPESA_CONSUMER_SECRET"]
    api_URL = app.config["MPESA_API_URL"] + app.config['MPESA_GRANT_TYPE']


class MpesaAccessToken:
    response = requests.get(
        MpesaC2BCredential.api_URL,
        auth=HTTPBasicAuth(
            MpesaC2BCredential.consumer_key,
            MpesaC2BCredential.consumer_secret))
    mpesa_access_token = json.loads(response.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']


class LipaNaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = app.config['MPESA_BUSINESS_SHORT_CODE']
    offset_value = '0'
    pass_key = app.config['MPESA_PASS_KEY']
    data_to_encode = business_short_code + pass_key + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_online_password = online_password.decode('utf-8')
