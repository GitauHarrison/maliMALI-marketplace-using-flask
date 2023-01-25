import africastalking
from app import app
from flask_login import current_user


def send_airtime():
    username = app.config['AT_USERNAME']
    api_key = app.config['AFRICASTALKING_API_KEY']

    africastalking.initialize(username, api_key)

    airtime = africastalking.Airtime

    phone_number = current_user.phone
    currency_code = "KES" #Change this to your country's code
    amount = 5

    try:
        response = airtime.send(
            phone_number=phone_number, amount=amount, currency_code=currency_code)
        print(response)
    except Exception as e:
        print(f"Encountered an error while sending airtime. More error details below\n {e}")
